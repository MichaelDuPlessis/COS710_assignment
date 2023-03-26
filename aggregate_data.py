#!/usr/bin/env python

# this is just used to aggregate the data from runs

import sys
import os
import json

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Incorrect number or args')
        print('Pass in 1 arg being the folder path')
    else:
        path = sys.argv[1]

        files_aggregated = 0
        aggregation = {
            'time': 0,
            'best': 0,
            'generations_completed': 0,
            'measures': {
                'training': {
                    'rmse': 0,
                    'r_squared': 0,
                    'median_absolute_error': 0,
                    'mean_absolute_error': 0
                },
                'testing': {
                    'rmse': 0,
                    'r_squared': 0,
                    'median_absolute_error': 0,
                    'mean_absolute_error': 0
                },
            },
            'best_overall': {}
        }

        best_mae = 999
        for _, _, files in os.walk(path):
            for file in files:
                files_aggregated += 1

                with open(os.path.join(path, file)) as f:
                    data = json.load(f)

                    aggregation['time'] += data['time']
                    aggregation['best'] += data['best']
                    aggregation['generations_completed'] += data['generations_completed']
                    aggregation['measures']['training']['rmse'] += data['measures']['training']['rmse']
                    aggregation['measures']['training']['r_squared'] += data['measures']['training']['r_squared']
                    aggregation['measures']['training']['median_absolute_error'] += data['measures']['training']['median_absolute_error']
                    aggregation['measures']['training']['mean_absolute_error'] += data['measures']['training']['mean_absolute_error']
                    aggregation['measures']['testing']['rmse'] += data['measures']['testing']['rmse']
                    aggregation['measures']['testing']['r_squared'] += data['measures']['testing']['r_squared']
                    aggregation['measures']['testing']['median_absolute_error'] += data['measures']['testing']['median_absolute_error']
                    aggregation['measures']['testing']['mean_absolute_error'] += data['measures']['testing']['mean_absolute_error']

                    if data['best'] < best_mae:
                        best_mae = data['best']

                        aggregation['best_overall'] = {
                            'best': data['best'],
                            'time': data['time'],
                            'generations_completed': data['generations_completed'],
                            'measures': data['measures'],
                        }

        aggregation['time'] /= files_aggregated
        aggregation['best'] /= files_aggregated
        aggregation['generations_completed'] /= files_aggregated
        aggregation['measures']['training']['rmse'] /= files_aggregated
        aggregation['measures']['training']['r_squared'] /= files_aggregated
        aggregation['measures']['training']['median_absolute_error'] /= files_aggregated
        aggregation['measures']['training']['mean_absolute_error'] /= files_aggregated
        aggregation['measures']['testing']['rmse'] /= files_aggregated
        aggregation['measures']['testing']['r_squared'] /= files_aggregated
        aggregation['measures']['testing']['median_absolute_error'] /= files_aggregated
        aggregation['measures']['testing']['mean_absolute_error'] /= files_aggregated

        with open(os.path.join('.', os.path.join(path.split(os.sep)[:-1].replace(os.sep, "")), '.json'), 'w') as of:
            json.dump(aggregation, of)