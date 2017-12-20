# Generic Importer Django module

This is a generic importer django module that can be used to
manage any kind of file. The idea is this module is a generic
interface to upload the file, and must be customized to
process the file and some minor changes.

# Instalation

To install this mudule you just need to copy the "importer"
folder to your django apps folder.

Then you must add a new url entry point to the urls.py file
of your main application. This module intention is to have
its entry at Django admin interface. Take care that the entry
must be loaded BEFORE the general "^admin/" url.
Example:
    url(r'^admin/importer/', include('importer.urls')),

Add the app to your application settings.py INSTALLED_APPS
array variable. You must add the following line in order to
make your app use the proper files and templates:
    INSTALLED_APPS = [
        ...
        'importer.apps.ImporterConfig',
        ...
    ]

You can configure your importer processes in importer/models.py
file. It will be created a importer type for each class.
All importer classes must have a 'process_file' method that will
receive as param the file name to use it at the import process.