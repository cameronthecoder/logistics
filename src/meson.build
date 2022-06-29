pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'logistics')
gnome = import('gnome')




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

logistics_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'docker.py'
]

install_data(logistics_sources, install_dir: moduledir)
