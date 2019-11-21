#!/usr/bin/env python3

import os
import sys
import yaml

from argparse import ArgumentParser


def main(args):
    """
    """
    parser = ArgumentParser(description='Create a HTML report page')
    parser.add_argument('input_dir',
                        type=str,
                        help='Dashboard directory')
    parser.add_argument('output',
                        type=str,
                        help='Output HTML file')
    args = parser.parse_args()

    input_dir = args.input_dir
    output_html = args.output
    dashboard_file = '{0}/dashboard.yml'.format(input_dir)

    # Collect any FP reports
    fp_reports = []
    for f in os.listdir(input_dir):
        if f.endswith('tsv'):
            fp_reports.append(f)

    # get the data from the dashboard
    with open(dashboard_file, 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)

    namespace = data['namespace']
    version_iri = data['version']
    date = data['date']
    summary = data['summary']
    results = data['results']

    with open(output_html, 'w+') as f:
        f.write('<head>\n')
        f.write('  <link rel="stylesheet" href=\
"https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">\n')
        f.write('  <title>{0} Dashboard Report</title>\n'.format(namespace))
        f.write('</head>\n')
        f.write('<body>\n')
        f.write('<div class="container">')
        f.write('<div class="row" style="padding-top:30px;">')
        f.write('<div class="col-md-2"></div>')
        f.write('<div class="col-md-8">')
        f.write('<h1>Dashboard Report - <a href=\
"http://obofoundry.org/ontology/{0}.html">{0}</a></h1>\n'.format(namespace))
        f.write('<p class="lead"><b>Version</b>: {0}<br>\n'.format(
            version_iri))
        f.write('<b>Date ran</b>: {0}</p>\n'.format(date))

        f.write('<p><center><small>Click on each link under "Check" to find \
            out more about the check and how to fix issues.<br>')
        f.write('Click on "View Report" under "Resources" for specific issues.\
            </small></center></p>')

        summary_status = summary['status']
        if 'comment' in summary:
            summary_comment = summary['comment']
        else:
            summary_comment = None

        # Alert box
        if summary_status == 'ERROR':
            alert = 'alert-danger'
        elif summary_status == 'WARN':
            alert = 'alert-warning'
        elif summary_status == 'INFO':
            alert = 'alert-info'
        else:
            alert = 'alert-primary'

        f.write('<div class="alert {0}"><center><h3>{1}'.format(
            alert, summary_status))
        if summary_comment:
            f.write(' - {0}</h3></center></div>\n'.format(summary_comment))
        else:
            f.write('</h3></center></div>\n')

        # Table headers
        f.write('<table class="table">\n')
        f.write('  <tr>\n')
        f.write('    <th>Check</th>\n')
        f.write('    <th>Status</th>\n')
        f.write('    <th>Comment</th>\n')
        f.write('    <th>Resources</th>\n')
        f.write('  </tr>\n')

        for check, details in results.items():
            f.write('  <tr>\n')
            file = None

            # ROBOT Report does not correspond to an FP
            if check != 'ROBOT Report':
                fp = check.split(' ')[0]
                check = check.split(' ', 1)[1]
            else:
                fp = None
                if 'robot_report.tsv' in fp_reports:
                    file = 'robot_report.html'

            # These checks might also have report files
            if fp == 'FP3' and 'fp3.tsv' in fp_reports:
                file = 'fp3.html'
            elif fp == 'FP7' and 'fp7.tsv' in fp_reports:
                file = 'fp7.html'

            status = details['status']
            if 'comment' in details:
                comment = details['comment']
            else:
                comment = ''

            # Get the CSS style for the status box
            if status in class_map:
                td_class = class_map[status]
            else:
                td_class = 'active'

            icon = None
            if status in icon_map:
                icon = '<img src="../assets/{0}.svg" height="15px">'.format(
                    icon_map[status])

            # Get the link to the check documentation
            if fp:
                url = principle_map[fp]
            else:
                # ROBOT Report link
                url = 'http://robot.obolibrary.org/report'

            # Write lines
            f.write('    <td><a href="{0}">{1}</a></td>\n'.format(url, check))

            if icon:
                f.write('    <td class="{0}" style="text-align:center;">\
                    {1}</td>'.format(td_class, icon))
            else:
                f.write('    <td class="{0}">{1}</td>'.format(
                    td_class, status))

            f.write('    <td>{0}</td>'.format(comment))
            if file:
                f.write('    <td><a href="{0}">View Report</a></td>'.format(
                    file))
            else:
                f.write('    <td></td>')
            f.write('  </tr>')
        f.write('</table>')
        f.write('</div></div></div>')
        f.write('</body>')


icon_map = {
    'PASS': 'check',
    'INFO': 'info',
    'WARN': 'warning',
    'ERROR': 'x'
}

# CSS classes for each level
class_map = {
    'PASS': 'table-success',
    'INFO': 'table-info',
    'WARN': 'table-warning',
    'ERROR': 'table-danger'
}

# map of principle keys to their doc links
principle_map = {
    'FP1': 'http://obofoundry.org/principles/checks/fp_001',
    'FP2': 'http://obofoundry.org/principles/checks/fp_002',
    'FP3': 'http://obofoundry.org/principles/checks/fp_003',
    'FP4': 'http://obofoundry.org/principles/checks/fp_004',
    'FP5': 'http://obofoundry.org/principles/checks/fp_005',
    'FP6': 'http://obofoundry.org/principles/checks/fp_006',
    'FP7': 'http://obofoundry.org/principles/checks/fp_007',
    'FP8': 'http://obofoundry.org/principles/checks/fp_008',
    'FP9': 'http://obofoundry.org/principles/checks/fp_009',
    'FP11': 'http://obofoundry.org/principles/checks/fp_011',
    'FP12': 'http://obofoundry.org/principles/checks/fp_012',
    'FP16': 'http://obofoundry.org/principles/checks/fp_016'
}

if __name__ == '__main__':
    main(sys.argv)
