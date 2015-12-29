#!/usr/bin/python
# coding: utf-8
import os
import sys
import re
import csv

# Generate pdf file
def export_pdf(filename, directory):
    print "    exporting pdf certificate from "+directory+"/"+filename+".pdf"
    command = 'inkscape %s.svg --export-pdf=%s/%s.pdf' % (filename, directory, filename)
    os.system(command)
    print "    removing svg file\n"
    if sys.platform == "win32": # Windows mode
        remove = 'del %s.svg' % (filename)
    else:                       # Unix mode
        remove = 'rm %s.svg' % (filename)
    os.system(remove)

# Modifies svg file copy
def modify_svg(svg_name, svg_file, filename, name):
    print "    copying the svg file from " + filename + ".svg"
    if sys.platform == "win32": # Windows mode
        command = 'copy %s.svg %s.svg' % (svg_name, filename)
    else:                       # Unix mode
        command = 'cp %s.svg %s.svg' % (svg_name, filename)
    os.system(command)

    # Including name
    new_certificate = open(filename + ".svg",'r+')
    new_certificate.write(re.sub("___NAME___", name, svg_file))
    new_certificate.close()

# Generate the certificates
def generate_certificates(svg_name, list_names_file, directory):
    svg_file = open(svg_name+".svg").read()  # Open and read the SVG file
    list_names = open(list_names_file)
    for name in list_names:
        name = name.rstrip("\n")
        if (name):
            print "Generating " + name + "'s certificate:\n"
            filename = name.replace(" ","_")
            modify_svg(svg_name, svg_file, filename, name)
            export_pdf(filename, directory)
            print "Finished\n\n"

# Main
if __name__ == '__main__':
    if(len(sys.argv) != 4):
        print "Usage: python g_certificates.py <svg_name> <list_of_names> <folder>"
        sys.exit()

    svg_name = sys.argv[1]  # Name of svg file
    list_names_file = sys.argv[2]  # List of names for generate the certificates
    directory = sys.argv[3]  # Directory for storage the certificates

    # Check files
    if not os.path.isfile(svg_name+".svg"):
        print "The "+svg_name+".svg file not found"
        sys.exit()
    if not os.path.isfile(list_names_file):
        print "The "+list_names_file+" file not found"
        sys.exit()

    # Check directory
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Check platform
    if sys.platform == "win32":
        print "Windows mode"
    else:
        print "Unix mode"

    generate_certificates(svg_name, list_names_file, directory)
