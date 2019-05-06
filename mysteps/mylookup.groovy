/**
This is the lookup functions implement by myself
*/

/**
get function calls by name and file
*/


Object.metaClass.getFunctionsByName = { name, honorVisibility = true ->
	getNodesWithTypeAndName(TYPE_FUNCTION, name, honorVisibility)
}


Object.metaClass.getCallsByFileAndName = { filename, name, honorVisibility = true ->
    getCallsTo(name)
}
