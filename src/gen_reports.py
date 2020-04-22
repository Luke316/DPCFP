import csv
from fractions import Fraction
from time import time
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from collections import OrderedDict

mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['font.size'] = 16


def plot_metrics(T_names, privacy, utility):
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    fig3, ax3 = plt.subplots(figsize=(6, 6))
    fig4, ax4 = plt.subplots(figsize=(6, 6))
    fig5, ax5 = plt.subplots(figsize=(6, 6))

    ax1.set_xlabel('Privacy Budget')
    ax1.set_ylabel('Precision')
    ax1.set_xlim(1, 5)
    ax1.set_ylim(0, 1)
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax1.grid(True, ls='--')

    ax2.set_xlabel('Privacy Budget')
    ax2.set_ylabel('Recall')
    ax2.set_xlim(1, 5)
    ax2.set_ylim(0, 1)
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax2.grid(True, ls='--')

    ax3.set_xlabel('Privacy Budget')
    ax3.set_ylabel('F Score')
    ax3.set_xlim(1, 5)
    ax3.set_ylim(0, 1)
    ax3.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax3.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    ax3.grid(True, ls='--')

    ax4.set_xlabel('Privacy Budget')
    ax4.set_ylabel('MAE')
    ax4.set_xlim(1, 5)
    ax4.set_ylim(0, 0.025)
    ax4.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax4.yaxis.set_major_locator(ticker.MultipleLocator(0.0025))
    ax4.grid(True, ls='--')

    ax5.set_xlabel('Privacy Budget')
    ax5.set_ylabel('MRE')
    ax5.set_xlim(1, 5)
    ax5.set_ylim(0, 0.15)
    ax5.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax5.yaxis.set_major_locator(ticker.MultipleLocator(0.015))
    ax5.grid(True, ls='--')

    for T_name in T_names:
        loss_mean, loss_std = [], []

        precision_mean, precision_std = [], []
        recall_mean, recall_std = [], []
        f_score_mean, f_score_std = [], []

        mae_mean, mae_std = [], []
        mre_mean, mre_std = [], []

        for i in range(len(privacy[T_name]['loss'])):
            loss_mean.append(np.mean(privacy[T_name]['loss'][i]))
            loss_std.append(np.std(privacy[T_name]['loss'][i]))

            precision_mean.append(np.mean(utility[T_name]['precision'][i]))
            precision_std.append(np.std(utility[T_name]['precision'][i]))

            recall_mean.append(np.mean(utility[T_name]['recall'][i]))
            recall_std.append(np.std(utility[T_name]['recall'][i]))

            f_score_mean.append(np.mean(utility[T_name]['f_score'][i]))
            f_score_std.append(np.std(utility[T_name]['f_score'][i]))

            mae_mean.append(np.mean(utility[T_name]['mae'][i]))
            mae_std.append(np.std(utility[T_name]['mae'][i]))

            mre_mean.append(np.mean(utility[T_name]['mre'][i]))
            mre_std.append(np.std(utility[T_name]['mre'][i]))

        if T_name == 'retail':
            fmt = 'ro-'
            label = T_name.title()
        elif T_name == 'BMS1':
            fmt = 'cs-'
            label = T_name
        elif T_name == 'BMS2':
            fmt = 'b^-'
            label = T_name
        elif T_name == 'ml-10M100K':
            fmt = 'gp-'
            label = 'Action'
        elif T_name == 'kosarak':
            fmt = 'yH-'
            label = T_name.title()
        elif T_name == 'BMS-POS':
            fmt = 'md-'
            label = T_name
        elif T_name == 'T10I4D100K':
            fmt = 'k*-'
            label = T_name



        ax1.errorbar(loss_mean, precision_mean, yerr=precision_std, fmt=fmt, fillstyle='none', label=label, capsize=5)
        ax2.errorbar(loss_mean, recall_mean, yerr=recall_std, fmt=fmt, fillstyle='none', label=label, capsize=5)
        ax3.errorbar(loss_mean, f_score_mean, yerr=f_score_std, fmt=fmt, fillstyle='none', label=label, capsize=5)
        ax4.errorbar(loss_mean, mae_mean, yerr=mae_std, fmt=fmt, fillstyle='none', label=label, capsize=5)
        ax5.errorbar(loss_mean, mre_mean, yerr=mre_std, fmt=fmt, fillstyle='none', label=label, capsize=5)

    ax1.legend(loc='lower right')
    ax2.legend(loc='lower right')
    ax3.legend(loc='lower right')
    ax4.legend(loc='lower right')
    ax5.legend(loc='lower right')

    fig1.tight_layout()  # rect=[0, 0.03, 1, 0.95] for suptitle
    fig2.tight_layout()
    fig3.tight_layout()
    fig4.tight_layout()
    fig5.tight_layout()

    fig1.savefig('..\\reports\\privacy_vs_precision.svg')
    fig2.savefig('..\\reports\\privacy_vs_recall.svg')
    fig3.savefig('..\\reports\\privacy_vs_F_score.svg')
    fig4.savefig('..\\reports\\privacy_vs_MAE.svg')
    fig5.savefig('..\\reports\\privacy_vs_MRE.svg')
    plt.show()


def gen_txt(T_names, privacy, utility):
    with open('..\\reports\\privacy_vs_utility.txt', 'w', newline=''):
        pass
    for T_name in T_names:
        losses =     ['Utility/Privacy   ']
        precisions = ['Precision         ']
        recalls =    ['Recall            ']
        f_scores =   ['F Score           ']
        maes =       ['MAE               ']
        mres =       ['MRE               ']

        for i in range(len(privacy[T_name]['loss'])):
            loss_mean = np.mean(privacy[T_name]['loss'][i])
            loss_std = np.std(privacy[T_name]['loss'][i])
            losses.append('{:.3f} ({:.3f})'.format(loss_mean, loss_std))

            precision_mean = np.mean(utility[T_name]['precision'][i])
            precision_std = np.std(utility[T_name]['precision'][i])
            precisions.append('{:.3f} ({:.3f})'.format(precision_mean, precision_std))

            recall_mean = np.mean(utility[T_name]['recall'][i])
            recall_std = np.std(utility[T_name]['recall'][i])
            recalls.append('{:.3f} ({:.3f})'.format(recall_mean, recall_std))

            f_score_mean = np.mean(utility[T_name]['f_score'][i])
            f_score_std = np.std(utility[T_name]['f_score'][i])
            f_scores.append('{:.3f} ({:.3f})'.format(f_score_mean, f_score_std))

            mae_mean = np.mean(utility[T_name]['mae'][i])
            mae_std = np.std(utility[T_name]['mae'][i])
            maes.append('{:.3f} ({:.3f})'.format(mae_mean, mae_std))

            mre_mean = np.mean(utility[T_name]['mre'][i])
            mre_std = np.std(utility[T_name]['mre'][i])
            mres.append('{:.3f} ({:.3f})'.format(mre_mean, mre_std))

        with open('..\\reports\\privacy_vs_utility.txt', 'a', newline='') as pu:
            if T_name == 'retail' or T_name == 'kosarak':
                pu.write(T_name.title())
            elif T_name == 'BMS1' or T_name == 'BMS2':
                pu.write(T_name)
            elif T_name == 'ml-10M100K':
                pu.write('Action')
            pu.write('\n')
            pu.write('  '.join(losses))
            pu.write('\n')
            pu.write('  '.join(precisions))
            pu.write('\n')
            pu.write('  '.join(recalls))
            pu.write('\n')
            pu.write('  '.join(f_scores))
            pu.write('\n')
            pu.write('  '.join(maes))
            pu.write('\n')
            pu.write('  '.join(mres))
            pu.write('\n\n')



    with open('..\\reports\\maximum_support_difference_vs_utility.txt', 'w', newline=''):
        pass
    for T_name in T_names:
        losses =     ['Privacy           ']
        rs =         ['Utility/MSD       ']
        precisions = ['Precision         ']
        recalls =    ['Recall            ']
        f_scores =   ['F Score           ']
        maes =       ['MAE               ']
        mres =       ['MRE               ']

        for i in range(len(phi_lst)):
            rs.append('{:.3f}        '.format(phi_lst[i]))

            loss_mean = np.mean(privacy[T_name]['loss'][i])
            loss_std = np.std(privacy[T_name]['loss'][i])
            losses.append('{:.3f} ({:.3f})'.format(loss_mean, loss_std))

            precision_mean = np.mean(utility[T_name]['precision'][i])
            precision_std = np.std(utility[T_name]['precision'][i])
            precisions.append('{:.3f} ({:.3f})'.format(precision_mean, precision_std))

            recall_mean = np.mean(utility[T_name]['recall'][i])
            recall_std = np.std(utility[T_name]['recall'][i])
            recalls.append('{:.3f} ({:.3f})'.format(recall_mean, recall_std))

            f_score_mean = np.mean(utility[T_name]['f_score'][i])
            f_score_std = np.std(utility[T_name]['f_score'][i])
            f_scores.append('{:.3f} ({:.3f})'.format(f_score_mean, f_score_std))

            mae_mean = np.mean(utility[T_name]['mae'][i])
            mae_std = np.std(utility[T_name]['mae'][i])
            maes.append('{:.3f} ({:.3f})'.format(mae_mean, mae_std))

            mre_mean = np.mean(utility[T_name]['mre'][i])
            mre_std = np.std(utility[T_name]['mre'][i])
            mres.append('{:.3f} ({:.3f})'.format(mre_mean, mre_std))

        with open('..\\reports\\maximum_support_difference_vs_utility.txt', 'a', newline='') as pu:
            if T_name == 'retail' or T_name == 'kosarak':
                pu.write(T_name.title())
            elif T_name == 'BMS1' or T_name == 'BMS2':
                pu.write(T_name)
            elif T_name == 'ml-10M100K':
                pu.write('Action')
            pu.write('\n')
            pu.write('  '.join(losses))
            pu.write('\n')
            pu.write('  '.join(rs))
            pu.write('\n')
            pu.write('  '.join(precisions))
            pu.write('\n')
            pu.write('  '.join(recalls))
            pu.write('\n')
            pu.write('  '.join(f_scores))
            pu.write('\n')
            pu.write('  '.join(maes))
            pu.write('\n')
            pu.write('  '.join(mres))
            pu.write('\n\n')