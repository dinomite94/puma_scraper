#!/usr/local/bin/python3
import argparse
import excel_exporter
import extractor
import json
import os
import re
import shutil
import subprocess
import sys


root_dir = os.path.dirname(os.path.realpath(__file__))
out_dir = os.path.join(root_dir, 'out')
out_jobs_dir = os.path.join(out_dir, 'jobs')


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        print(stdout_line) 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def run(args):
    execute(['scrapy', 'crawl', 'index'])
    execute(['scrapy', 'crawl', 'job'])
    process(args)
    compress(args)


def clean(args):
    raise NotImplementedError()


def compress(args):
    shutil.make_archive(out_jobs_dir, 'zip', out_jobs_dir)


def crawl(args):
    raise NotImplementedError()


def process(args):
    data = []

    for filename in os.listdir(out_jobs_dir):
        if str.endswith(filename, '.json'):
            full_filename = os.path.join(out_jobs_dir, filename)
            with open(full_filename, 'r') as f:
                fileid = os.path.basename('.'.join(filename.split('.')[:-1]))
                row = extractor.processJSON(json.load(f))
                row.extend((
                    excel_exporter.HyperLink(text='Screenshot', link='{}.png'.format(fileid)),
                    excel_exporter.HyperLink(text='Lokal', link='{}.html'.format(fileid)),
                    excel_exporter.HyperLink(text='Online', link='https://about.puma.com/en/jobs/{}'.format(fileid))
                ))

                data.append(row)

    excel_exporter.export(data)


cmds = {
    'run': run,
    'clean': clean,
    'compress': compress,
    'crawl': crawl,
    'process': process,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Puma Job Offers Crawler')
    subparsers = parser.add_subparsers(help='sub-command help')
    subparsers.required = False
    
    subparsers.add_parser('run', help='Run crawler and process')
    subparsers.add_parser('fix-html', help='Run crawler and process')
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
