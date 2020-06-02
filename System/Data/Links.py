class Links:
    ip = "localhost"
    getLessThan3Duplication = "http://"+ip+"/master_tracker/get_nodes_less_duplication.php"
    updateDuplication = "http://" + ip + "/master_tracker/update_duplication.php"
    addFileDup = "http://" + ip + "/master_tracker/insert_file.php"
    getFiles = "http://" + ip + "/master_tracker/get_files.php"
    getNodesContainsFile = "http://" + ip + "/master_tracker/get_nodes_contain_file.php"
    deleteNoDuplicationHappend = "http://" + ip + "/master_tracker/deleteInLast6HoursNotActivated.php"
    deleteNode = "http://" + ip + "/master_tracker/deleteNode.php"

