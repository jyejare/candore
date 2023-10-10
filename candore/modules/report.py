"""Centralized Reporting utilities for compared results"""
import json
import csv
from pathlib import Path
# from .webapp import display_json_table, render_webpage


class Reporting:
    """Centralized Reporting utilities for compared results"""

    def __init__(self, results):
        """Initialize the Reporting class

        Args:
            comparator (Comparator): The comparator object to use for reporting
        """
        self.results = results

    def generate_report(self, output_file, output_type):
        """Generate a report of the compared results

        Args:
            output_file (str): The file to write the report to
            output_type (str): The type of report to generate (json, CSV or Web)
        Returns:
            None
        Raises:
            ValueError: If the output_type is not supported
        """
        if output_type == 'json':
            self._generate_json_report(output_file)
        elif output_type == 'html':
            self._generate_html_report()
        elif output_type == 'csv':
            self._generate_csv_report(output_file)
        else:
            raise ValueError("Output type {} not supported".format(output_type))

    def _generate_json_report(self, output_file):
        """Generate a JSON report of the compared results

        Args:
            output_file (str): The file to write the report to
        Returns:
            None
        """
        if not output_file:
            output_file = 'results.json'
        output_file = Path(output_file)
        # Write the JSON report to the output file
        output_file.write_text(json.dumps(self.results, indent=4))
        print("Wrote JSON report to {}".format(output_file))
        print("JSON report contains {} results".format(len(self.results)))

    def _generate_html_report(self):
        """Generate an HTML report of the compared results

        Args:
            output_file (str): The file to write the report to
        Returns:
            None
        """
        #display_json_table(results_json=self.results)
        #render_webpage()
        print("HTML report is ready to view at: http://localhost:5000")

    def _generate_csv_report(self, output_file):
        """Generate a CSV report of the compared results

        Args:
            output_file (str): The file to write the report to
        Returns:
            None
        """
        if not output_file:
            output_file = 'results.csv'
        output_file = Path(output_file)
        # Convert json to csv and write to output file
        csv_writer = csv.writer(output_file.open('w'))
        csv_writer.writerow(['Variation Path', 'Pre-Upgrade', 'Post-Upgrade', 'Variation'])
        for var_path, vals in self.results.items():
            csv_writer.writerow([var_path, vals['pre'], vals['post'], vals['variation']])
        print("Wrote CSV report to {}".format(output_file))
        print("CSV report contains {} results".format(len(self.results)))

