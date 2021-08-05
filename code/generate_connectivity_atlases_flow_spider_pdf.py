#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fpdf import FPDF
import sys
import os


def parse_report(filename):
    f = open(filename, "r")

    lines = f.readlines()
    final = []
    for i, line in enumerate(lines):
        if 'Run times' in line:
            tmp_1, tmp_2 = lines[i+2].split(' - ')
            tmp_1 = tmp_1.replace('<span id="workflow_start">', '')
            tmp_1 = tmp_1.replace('</span>', '').strip()
            tmp_2 = tmp_2.replace('<span id="workflow_complete">', '')
            tmp_2 = tmp_2.replace('</span>', '').strip()
            final.append(tmp_1)
            final.append(tmp_2)
        elif 'CPU-Hours' in line:
            tmp = lines[i+1].replace('<dd class="col-sm-9"><samp>', '')
            tmp = tmp.replace('</samp></dd>', '').strip()
            final.append(tmp+' hours')
        elif 'Nextflow command' in line:
            tmp = lines[i+1].replace('<dd><pre class="nfcommand"><code>', '')
            tmp = tmp.replace('</code></pre></dd>', '').strip()
            final.append(tmp)
        elif 'Workflow execution' in line:
            tmp = lines[i].strip().replace('</h4>', '')
            tmp = tmp.replace('<h4>', '')
            final.append(tmp)

    return final


class PDF(FPDF):
    def titles(self, title, width=210, pos_x=0, pos_y=0):
        self.set_xy(pos_x, pos_y)
        self.set_font('Arial', 'B', 16)
        self.multi_cell(w=width, h=20.0, align='C', txt=title,
                        border=0)

    def add_cell_left(self, title, text, size_y=10, width=200):
        self.set_xy(5.0, self.get_y() + 4)
        self.set_font('Arial', 'B', 12)
        self.multi_cell(width, 5, align='L', txt=title)
        self.set_xy(5.0, self.get_y())
        self.set_font('Arial', '', 10)
        self.multi_cell(width, size_y, align='L', txt=text, border=1)

    def init_pos(self, pos_x=None, pos_y=None):
        pos = [0, 0]
        pos[0] = pos_x if pos_x is not None else 10
        pos[1] = pos_y if pos_y is not None else self.get_y()+10
        return pos

    def add_image(self, title, filename, size_x=75, size_y=75,
                  pos_x=None, pos_y=None):
        pos = self.init_pos(pos_x, pos_y)
        self.set_xy(pos[0], pos[1])
        self.set_font('Arial', 'B', 12)
        self.multi_cell(size_x, 5, align='C', txt=title)
        self.image(filename, x=pos[0], y=pos[1]+5,
                   w=size_x, h=size_y, type='PNG')
        self.set_y(pos[1]+size_y+10)

    def add_mosaic(self, main_tile, titles, filenames, size_x=75, size_y=75,
                   row=1, col=1, pos_x=None, pos_y=None):
        pos = self.init_pos(pos_x, pos_y)
        self.set_xy(pos[0], pos[1])
        self.set_font('Arial', 'B', 12)
        self.multi_cell(size_x*col, 5, align='C', txt=main_tile)

        for i in range(row):
            for j in range(col):
                self.set_xy(pos[0]+size_x*j, pos[1]+5+size_y*i)
                self.set_font('Arial', '', 10)
                self.multi_cell(size_x, 5, align='C', txt=titles[j+col*i])
                self.image(filenames[j+col*i],
                           x=pos[0]+size_x*j, y=pos[1]+10+size_y*i,
                           w=size_x, h=size_y, type='PNG')
        self.set_y(pos[1]+(size_y*row)+10)


html_info = parse_report('report.html')
METHODS = """This pipeline facilitates the creation of atlases for Connectoflow [1].
It creates atlases from the Freesurfer output: Brainnetome [2], Glasser [3], Schaefer[4],
Lausanne multi-scales [5] and lobes. All atlases are free of WM and CSF labels, ready for connectomics.
All output atlases have the following files associated with them:
- atlas_*_v4.nii.gz (parcellation as computed)
- atlas_*_v4_dilate.nii.gz (parcellation with cortical labels dilate into the WM)
- atlas_*_v4_LUT.json (Links the labels number to its name)
- atlas_*_v4_LUT.txt (Links the labels number to its name and color scheme for Freeview)
- atlas_*_v4_labels_list.txt (Contains the list of expected labels number)
"""

REFERENCES = """[1] Rheault, Francois, et al. "Connectoflow: A cutting-edge Nextflow pipeline for structural connectomics",
    ISMRM 2021 Proceedings, #710.
[2] Fan, Lingzhong, et al. "The human brainnetome atlas: a new brain atlas based on connectional architecture.",
    Cerebral cortex 26.8 (2016): 3508-3526.
[3] Glasser, Matthew F., et al. "A multi-modal parcellation of human cerebral cortex.",
    Nature 536.7615 (2016): 171-178.
[4] Schaefer, Alexander, et al. "Local-global parcellation of the human cerebral cortex from intrinsic functional connectivity MRI.",
    Cerebral cortex 28.9 (2018): 3095-3114.
[5] Tourbier, Sebastien et al. "Multi-scale-brain-parcellator-a-bids-app-for-the-lausanne-connectome-parcellation",
    OHBM 2019 Annual Meeting.
"""

pdf = PDF(orientation='P', unit='mm', format='A4')
pdf.add_page()
pdf.titles('Connectivity_Atlases_Flow_V1: {}'.format(sys.argv[2]))
pdf.add_cell_left('Status:', html_info[0], size_y=5)
pdf.add_cell_left('Started on:', html_info[1], size_y=5)
pdf.add_cell_left('Completed on:', html_info[2], size_y=5)
pdf.add_cell_left('Command:', html_info[3], size_y=5)
pdf.add_cell_left('Duration:', html_info[4], size_y=5)

pdf.add_cell_left('Methods:', METHODS, size_y=5)
pdf.add_cell_left('References:', REFERENCES, size_y=5)

pdf.add_page()
pdf.titles('Connectivity_Atlases_Flow_V1: {}'.format(sys.argv[2]))
pdf.add_image('Freesurfer', '{}/atlas_freesurfer_v4.png'.format(sys.argv[1]), size_x=175, size_y=220)
pdf.add_page()
pdf.add_image('Brainnetome', '{}/atlas_brainnetome_v4.png'.format(sys.argv[1]), size_x=175, size_y=220)
pdf.add_page()
pdf.add_image('Glasser', '{}/atlas_glasser_v4.png'.format(sys.argv[1]), size_x=175, size_y=220)
pdf.add_page()
pdf.add_image('Schaefer_100', '{}/atlas_schaefer_100_v4.png'.format(sys.argv[1]), size_x=175, size_y=220)
pdf.output('{}/report.pdf'.format(sys.argv[1], 'F'))
