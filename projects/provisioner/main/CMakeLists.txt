set(srcs "main.c")

idf_component_register(SRCS "node_info.c" "${srcs}" "ble_mesh_provisioner.c"
                    INCLUDE_DIRS  ".")
