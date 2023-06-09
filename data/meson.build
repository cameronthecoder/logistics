desktop_file = i18n.merge_file(
  input: 'com.camerondahl.Logistics.desktop.in',
  output: 'com.camerondahl.Logistics.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'logistics')
gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'ui/window.bp',
    'ui/container_details_view.bp',
    'ui/container_logs_page.bp',
    'ui/container_row.bp',
    'ui/preferences.bp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('logistics',
  'logistics.gresource.xml',
  gresource_bundle: true,
  install: true,
  dependencies: [blueprints],
  install_dir: pkgdatadir,
)


desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils,
    args: [desktop_file]
  )
endif



appstream_file = i18n.merge_file(
  input: 'com.camerondahl.Logistics.appdata.xml.in',
  output: 'com.camerondahl.Logistics.appdata.xml',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'appdata')
)

appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util,
    args: ['validate', appstream_file]
  )
endif

install_data('com.camerondahl.Logistics.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file', compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
endif

subdir('icons')

gnome = import('gnome')

gnome.post_install(
  glib_compile_schemas: true,
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)
