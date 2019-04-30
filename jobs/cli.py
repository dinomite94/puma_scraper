#!/usr/local/bin/python3
import argparse
import excel_exporter
import extractor
import json
import os
import shutil
import subprocess
import sys


root_dir = os.path.dirname(os.path.realpath(__file__))
out_dir = os.path.join(root_dir, 'out')
out_jobs_dir = os.path.join(out_dir, 'jobs')


def clean(args):
    pass


def compress(args):
    shutil.make_archive(out_jobs_dir, 'zip', out_jobs_dir)


def crawl(args):
    pass


def process(args):
    data = []

    for filename in os.listdir(out_jobs_dir):
        if str.endswith(filename, '.json'):
            full_filename = os.path.join(out_jobs_dir, filename)
            with open(full_filename, 'r') as f:
                fileid = os.path.basename('.'.join(filename.split('.')[:-1]))
                row = extractor.processJSON(json.load(f))
                row.extend((
                    excel_exporter.HyperLink(text='Screenshot', link='jobs/{}.png'.format(fileid)),
                    excel_exporter.HyperLink(text='Lokal', link='jobs/{}.html'.format(fileid)),
                    excel_exporter.HyperLink(text='Online', link='https://about.puma.com/en/jobs/r874'))
                )

                data.append(row)

    excel_exporter.export(data)


cmds = {
    'clean': clean,
    'compress': compress,
    'crawl': crawl,
    'process': process,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Puma Job Offers Crawler')
    subparsers = parser.add_subparsers(help='sub-command help')
    subparsers.required = False
    
    subparsers.add_parser('clean', help='Clean the output directory')
    subparsers.add_parser('compress', help='Create archive of output directory')

    crawl_parser = subparsers.add_parser('crawl', help='Run scrapy crawler for new data')
    crawl_parser.add_argument('--url', help='List of job openings (default: https://about.puma.com/en/careers/job-openings#jobfinder)')
    crawl_parser.add_argument('-no-html', type=bool, help='Do NOT save the HTML website')
    crawl_parser.add_argument('-no-screenshots', type=bool, help='Do NOT save the screenshots')
    crawl_parser.add_argument('-no-json', type=bool, help='Do NOT save JSON data')

    process_parser = subparsers.add_parser('process', help='Process crawled data')
    process_parser.add_argument('--process', type=bool, help='Process crawled data')
    process_parser.add_argument('-offline-html', type=bool, help='Preparate saved HTML website to work offline')
    process_parser.add_argument('-export-xlsx', type=bool, help='Process saved JSON data and fill Excel Sheet')

    args = parser.parse_args()

    if args:
        cmds[sys.argv[1]](args)
