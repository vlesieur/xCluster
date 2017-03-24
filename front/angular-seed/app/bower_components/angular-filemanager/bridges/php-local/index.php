<?php
namespace AngularFilemanager\LocalBridge;



/**
 *  PHP Local filesystem bridge for angular-filemanager
 *  
 *  @author Jakub Ďuraš <jakub@duras.me>
 *  @version 0.1.0
 */
include 'LocalBridge/Response.php';
include 'LocalBridge/Rest.php';
include 'LocalBridge/Translate.php';
include 'LocalBridge/FileManagerApi.php';

$basePath = '../../../../storage/user';
$fileManagerApi = new FileManagerApi($basePath,'en', false);

$rest = new Rest();
$rest->post([$fileManagerApi, 'postHandler'])
     ->get([$fileManagerApi, 'getHandler'])
     ->handle();