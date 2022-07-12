project('logistics',
          version: '0.1.0',
    meson_version: '>= 0.59.0',
  default_options: [ 'warning_level=2',
                     'werror=false',
                   ],
)

i18n = import('i18n')


pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
subdir('data')


python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)


configure_file(
  input: 'logistics.in',
  output: 'logistics',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)


install_subdir('logistics', install_dir: pkgdatadir)

subdir('po')
