<?php
$data = array();
$id = '0';
if (isset($_POST['id'])) {
    $id = $_POST['id'];
}
/*
if (isset($_GET['id'])) {
    $id = $_GET['id'];
}
*/
$act = False;
if (isset($_GET['act'])) {
    $act = $_GET['act'];
}

if (isset($_FILES['tpl-file'])) {
    $data['tpl'] = basename($_FILES['tpl-file']['name']);
    //$data['tpl'] = 'test-tpl';
}
// print_r($_FILES);


if ($id) {
    $data['id'] = $id;
    $path_in = 'uploads/'.$id.'/IN/';
    if ($act == 'uploadfile' and isset($_FILES['files'])) {
        $error = FALSE;
        $files = array();
        $uploaddir = './uploads/'.$id.'/IN/';
        if (!is_dir($uploaddir)) {
            if (!mkdir($uploaddir, 0777, TRUE)) { $data['message'][] = 'Impossible de créer le répertoire '.$uploaddir.'.'; }
        }
        $file = $_FILES['files'];
        if(move_uploaded_file($file['tmp_name'][0], $uploaddir.basename($file['name'][0]))) {
            $data['file'] = $file;
        } else {
            $error = TRUE;
        }
        if ($error) {
            $data['message'][] = 'Impossible de télécharger le fichier '.basename($file['name'][0]).'.';
        } else {
            $data['message'][] = 'Fichier téléchargé.';
        }
    } elseif ($act == 'submit') {
        // Zip files
        $error = FALSE;
        $filename = $path_in."mdConverter.zip";

        $zip = new ZipArchive();
        if ($zip->open($filename, ZipArchive::CREATE)!== TRUE) {
            $error = TRUE;
        }

        if (!$error) {
            foreach (glob($path_in."*.{xls,xlsx,XLS,XLSX}", GLOB_BRACE) as $f) {
                $zip->addFile($f, basename($f));
            }
            $data['nb_files'] = $zip->numFiles;
            $data['success'] = $zip->status;
            
            $zip->close();
        } else {
            $data['success'] = False;
        }
    }
}
echo json_encode($data);

?>
