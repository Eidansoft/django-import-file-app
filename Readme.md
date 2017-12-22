# Generic Importer Django module

This is a generic importer django module that can be used to
manage any kind of file. The idea of this module is to be a
generic interface to upload any file, and must be customized to
process the file and some other minor changes.

# Instalation steps

First to install this module you just need to copy the 'importer'
folder to your Django apps folder.

Then you must add a new url entry point to the 'urls.py' file
of your main Django application. This module intention is to have
its entry at Django admin interface. Take care that the entry
must be loaded BEFORE the general '^admin/' url.

Example:

    url(r'^admin/importer/', include('importer.urls')),

Add the app to your application 'settings.py' INSTALLED_APPS
array variable. You must add the following line in order to
make your app use the proper files and templates:

    INSTALLED_APPS = [
        ...
        'importer.apps.ImporterConfig',
        ...
    ]

Just with those simple steps you will have a up&running import
section into your Django admin main page.

# Customization of your imports

You can easily customize your importer processes in 'importer/models.py'
file. Just edit the default 'Example_Importer' class to fits your needs.
And you can create as many '_Importer' classes as you want, and you will
have multiple import managers.
The only requirement is that your customized importing classes must have
the suffix '_Importer' at class name, in order be identified and extend
'ImporterBase' class.
All '_Importer' classes must override the method 'process_file' method that
will receive as param the 'request'.

# Customization of the form

The default form only have a single input file. You can use any other form
at your '_Importer' class simply overriding the 'get_form' method. And you
will receive all your new input fields at the request param at the
'process_file' method in your import class.