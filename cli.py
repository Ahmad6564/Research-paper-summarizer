#!/usr/bin/env python3
"""
Command Line Interface for PaperSummarizer
"""

import argparse
import json
import sys
import os
from paper_summarizer import PaperSummarizer


def main():
    parser = argparse.ArgumentParser(
        description='PaperSummarizer - Academically rigorous research paper analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --pdf paper.pdf --output summary.md
  %(prog)s --url https://arxiv.org/abs/2301.00001 --json-output data.json
  %(prog)s --text "paper content..." --title "My Paper" --authors "John Doe"
        """
    )
    
    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--pdf', type=str, help='Path to PDF file')
    input_group.add_argument('--url', type=str, help='URL to paper (ArXiv, etc.)')
    input_group.add_argument('--text', type=str, help='Raw paper text')
    input_group.add_argument('--text-file', type=str, help='Path to text file')
    
    # Metadata options
    parser.add_argument('--title', type=str, help='Paper title')
    parser.add_argument('--authors', type=str, help='Paper authors')
    parser.add_argument('--venue-year', type=str, help='Venue and year (e.g., "ICML 2023")')
    parser.add_argument('--doi-arxiv', type=str, help='DOI or ArXiv ID')
    
    # Output options
    parser.add_argument('--output', '-o', type=str, help='Output file for Markdown summary')
    parser.add_argument('--json-output', '-j', type=str, help='Output file for JSON data')
    parser.add_argument('--print-markdown', action='store_true', help='Print Markdown to stdout')
    parser.add_argument('--print-json', action='store_true', help='Print JSON to stdout')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress progress messages')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not any([args.output, args.json_output, args.print_markdown, args.print_json]):
        parser.error("At least one output option must be specified")
    
    # Initialize summarizer
    if not args.quiet:
        print("Initializing PaperSummarizer...")
    
    try:
        summarizer = PaperSummarizer()
    except Exception as e:
        print(f"Error initializing summarizer: {e}", file=sys.stderr)
        return 1
    
    # Prepare metadata
    metadata = {}
    if args.title:
        metadata['title'] = args.title
    if args.authors:
        metadata['authors'] = args.authors
    if args.venue_year:
        metadata['venue_year'] = args.venue_year
    if args.doi_arxiv:
        metadata['doi_or_arxiv'] = args.doi_arxiv
    
    # Determine input source and type
    if args.pdf:
        if not os.path.exists(args.pdf):
            print(f"Error: PDF file not found: {args.pdf}", file=sys.stderr)
            return 1
        input_source = args.pdf
        input_type = 'pdf'
        if not args.quiet:
            print(f"Processing PDF: {args.pdf}")
    
    elif args.url:
        input_source = args.url
        input_type = 'url'
        if not args.quiet:
            print(f"Fetching from URL: {args.url}")
    
    elif args.text:
        input_source = args.text
        input_type = 'text'
        if not args.quiet:
            print("Processing provided text...")
    
    elif args.text_file:
        if not os.path.exists(args.text_file):
            print(f"Error: Text file not found: {args.text_file}", file=sys.stderr)
            return 1
        try:
            with open(args.text_file, 'r', encoding='utf-8') as f:
                input_source = f.read()
            input_type = 'text'
            if not args.quiet:
                print(f"Processing text file: {args.text_file}")
        except Exception as e:
            print(f"Error reading text file: {e}", file=sys.stderr)
            return 1
    
    # Process the paper
    try:
        if not args.quiet:
            print("Analyzing paper... This may take a few moments.")
        
        result = summarizer.summarize_paper(input_source, input_type, metadata)
        
        if not args.quiet:
            print("Analysis complete!")
        
    except Exception as e:
        print(f"Error processing paper: {e}", file=sys.stderr)
        return 1
    
    # Output results
    try:
        # Save Markdown output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result['markdown'])
            if not args.quiet:
                print(f"Markdown summary saved to: {args.output}")
        
        # Save JSON output
        if args.json_output:
            with open(args.json_output, 'w', encoding='utf-8') as f:
                json.dump(result['json'], f, indent=2, ensure_ascii=False)
            if not args.quiet:
                print(f"JSON data saved to: {args.json_output}")
        
        # Print to stdout
        if args.print_markdown:
            print("\n" + "="*80)
            print("MARKDOWN SUMMARY")
            print("="*80)
            print(result['markdown'])
        
        if args.print_json:
            print("\n" + "="*80)
            print("JSON DATA")
            print("="*80)
            print(json.dumps(result['json'], indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"Error saving output: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
