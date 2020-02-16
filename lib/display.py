#!/usr/bin/env python3
"""
Display library

Copyright (c) 2020 Nicolas Beguier
Licensed under the MIT License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Own library
# pylint: disable=E0401
import lib.analysis as analysis

def print_report(report, mic='XPAR', header=True, footer=True):
    """
    Prints the report
    """
    # TITLE
    print('ISIN: {}'.format(report['isin']))
    # HEADER
    if header:
        if 'nom' in report:
            print('Nom: {}'.format(report['nom']))
        if 'secteur' in report:
            print('Secteur: {}'.format(report['secteur']))
        if 'valorisation' in report:
            print('Valorisation: {} EUR'.format(report['valorisation']))
            print('Variation 1 an: {} %'.format(report['valorisation_1an']))
        if 'Dividendes' in report:
            print('|| Dividendes: {} EUR'.format(report['Dividendes']))
            print('|| PER: {} ({})'.format(report['PER'], analysis.per_text(report['PER'])))
            print('|| PEG: {} ({})'.format(report['PEG'], analysis.peg_text(report['PEG'])))
            print('|| Rendement: {} %'.format(report['Rendement']))
            print('|| Détachement: {}'.format(report['Détachement']))
            print('|| Prochain rdv: {}'.format(report['Prochain rdv']))
    # BODY
    if 'dividendes_history' in report:
        print('[Dividendes History] [{}] Rendement: {} %'.format(
            report['dividendes_history']['last_year'],
            report['dividendes_history']['last_rendement']))
        print('[Dividendes History] [{}] Valorisation: {} EUR'.format(
            report['dividendes_history']['last_year'],
            report['dividendes_history']['average_val']))
        print('[Dividendes History] [{}] Valorisation: {} EUR'.format(
            report['dividendes_history']['last_detach'],
            report['dividendes_history']['last_val']))
        print('[Dividendes History] [{}] Valorisation: {} EUR'.format(
            report['dividendes_history']['latest_detach'],
            report['dividendes_history']['latest_val']))
    if 'per_history' in report:
        print_per(report['per_history'], header)
    if 'peg_history' in report:
        print_peg(report['peg_history'], header)
    # FOOTER
    if footer:
        print('==============')
        if report['url'] is not None:
            print('Les Echos: {}'.format(report['url']))
        if mic == 'XPAR':
            print('Recapitulatif dividendes: https://www.bnains.org' +
                  '/archives/action.php?' +
                  'codeISIN={}'.format(report['isin']))
            print('Palmares CAC40 dividendes: https://www.boursorama.com' +
                  '/bourse/actions/palmares/dividendes/?market=1rPCAC&variation=6')
    print('==============')

def print_per(pers, header):
    """
    Prints PER informations
    """
    for per in pers:
        if pers[per]['current']:
            if not header:
                print('[PER History] PER {} actuel: {} EUR'.format(
                    round(per, 1),
                    round(pers[per]['value'], 2)))
        else:
            print('[PER History] [{}] PER {} ({}): {} EUR'.format(
                pers[per]['date'],
                per,
                analysis.per_text(per),
                round(pers[per]['value'], 2)))

def print_peg(pegs, header):
    """
    Prints PEG informations
    """
    for peg in pegs:
        if pegs[peg]['current']:
            if not header:
                print('[PEG History] PEG {} actuel: {} EUR'.format(
                    round(peg, 1),
                    round(pegs[peg]['value'], 2)))
        else:
            print('[PEG History] [{}] PEG {} ({}): {} EUR'.format(
                pegs[peg]['date'],
                peg,
                analysis.peg_text(peg),
                round(pegs[peg]['value'], 2)))

def print_health(report, verbose):
    """
    Prints the health status
    """
    if 'PER' not in report or 'PEG' not in report:
        print(False)
    if analysis.per_text(report['PER']) == 'ration bon' \
        and analysis.peg_text(report['PEG']) == 'croissance annoncée ok':
        if verbose:
            print(analysis.per_text(report['PER']), analysis.peg_text(report['PEG']))
        return print(True)
    return print(False)