if (NOT NOSE_FOUND)

	find_program(NOSE_EXECUTABLE nosetests)
	set(NOSE_EXECUTABLE ${NOSE_EXECUTABLE} CACHE STRING "")

# handle the QUIETLY and REQUIRED arguments and set NOSE_FOUND to TRUE if
# all listed variables are TRUE
    INCLUDE(FindPackageHandleStandardArgs)
    FIND_PACKAGE_HANDLE_STANDARD_ARGS(Nose DEFAULT_MSG NOSE_EXECUTABLE)

    mark_as_advanced(NOSE_FOUND NOSE_EXECUTABLE)


endif (NOT NOSE_FOUND)

