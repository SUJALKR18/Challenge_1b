"""
output_builder.py

This module contains the OutputBuilder class, which is responsible for the
final step of the pipeline: generating the JSON output file.

It takes the processed data structures and formats them into a dictionary that
strictly conforms to the required output specification, then writes it to a file.
"""
import json
import os
import re
from typing import List, Dict
from data_structures import Section, SystemInput, FinalOutput

class OutputBuilder:
    """
    Constructs and writes the final JSON output file.
    """
    def __init__(self, system_input: SystemInput):
        """
        Initializes the builder with the original system inputs for metadata.

        Args:
            system_input (SystemInput): The object containing the initial persona,
                                        job-to-be-done, and list of PDF paths.
        """
        self.input_metadata = {
            "input_documents": [os.path.basename(p) for p in system_input.pdf_paths],
            "persona": system_input.persona,
            "job_to_be_done": system_input.job_to_be_done
        }
        print("Output Builder initialized.")

    def build(self, ranked_sections: List[Section], sub_section_analysis: List[Dict]) -> FinalOutput:
        """
        Assembles the final output object from the processed data.

        Args:
            ranked_sections (List[Section]): The globally sorted list of sections.
            sub_section_analysis (List[Dict]): The detailed analysis of top sections.

        Returns:
            FinalOutput: A dataclass instance representing the complete JSON structure.
        """
        print("Building final output structure...")
        
        # Format the extracted sections list to match required structure (top 5 only)
        extracted_sections_list = []
        for section in ranked_sections[:5]:  # Only top 5 sections
            extracted_sections_list.append({
                "document": section.source_doc_name,
                "section_title": section.title,
                "importance_rank": section.rank,
                "page_number": section.page_number
            })
            
        # Format the subsection analysis to match required structure
        formatted_subsection_analysis = []
        for analysis in sub_section_analysis:
            # Clean up the text by removing excessive newlines and formatting
            cleaned_text = analysis["refined_text_snippet"]
            # Replace multiple newlines with single newlines
            cleaned_text = re.sub(r'\n+', '\n', cleaned_text)
            # Remove leading/trailing whitespace
            cleaned_text = cleaned_text.strip()
            
            formatted_subsection_analysis.append({
                "document": analysis["source_document"],
                "refined_text": cleaned_text,
                "page_number": ranked_sections[analysis["importance_rank"] - 1].page_number
            })
            
        final_output = FinalOutput(
            metadata=self.input_metadata,
            extracted_sections=extracted_sections_list,
            sub_section_analysis=formatted_subsection_analysis
        )
        
        return final_output

    def write_to_file(self, final_output: FinalOutput, output_path: str = "output.json"):
        """
        Serializes the final output object to a JSON file.

        Args:
            final_output (FinalOutput): The complete output data object.
            output_path (str): The path to write the final JSON file to.
        """
        print(f"Writing final output to {output_path}...")
        
        # Convert dataclass to a dictionary for JSON serialization
        output_dict = {
            "metadata": final_output.metadata,
            "extracted_sections": final_output.extracted_sections,
            "subsection_analysis": final_output.sub_section_analysis
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                # indent=4 makes the output human-readable, which is good practice
                json.dump(output_dict, f, indent=4, ensure_ascii=False)
            print("Successfully wrote JSON output.")
        except IOError as e:
            print(f"Error writing to file {output_path}: {e}")
            
