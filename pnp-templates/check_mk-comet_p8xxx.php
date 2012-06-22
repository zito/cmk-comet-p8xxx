<?php

# Template:	check_mk-comet_p8xxx.php
# Author:	vaclav.ovsik@gmail.com

# DS
#   1 temp

$_WARNRULE = '#FFFF00';
$_CRITRULE = '#FF0000';

$ds_name[1] = "Temperature";
$opt[1] = "--vertical-label '°C' --title \"$hostname / $servicedesc\" ";
$def[1] = rrd::def("temp", $RRDFILE[1], $DS[1], "AVERAGE");
$def[1] .= rrd::line1("temp", "#050", "temperature");
$def[1] .= rrd::gprint("temp", array("LAST", "MIN", "MAX", "AVERAGE"), "%3.1lf°C");

$lc = $CRIT_MIN[1];
$hc = $CRIT_MAX[1];
$lw = $WARN_MIN[1];
$hw = $WARN_MAX[1];
if ( $hc == null ) { $hc = $CRIT[1]; }
if ( $hw == null ) { $hw = $WARN[1]; }

$adef = array();
$nl = "\\n";
$nlevel = 0;
if ($hc != null) {
    array_push($adef, rrd::hrule($hc, $_CRITRULE, sprintf("Critical above %.1f°C$nl", $hc)));
    $nl = "";
    $nlevel++;
}
if ($lc != null) {
    array_push($adef, rrd::hrule($lc, $_CRITRULE, sprintf("Critical below %.1f°C$nl", $lc)));
    $nl = "";
    $nlevel++;
}
if ($nlevel > 1) {
    $nl = "\\n";
}
if ($hw != null) {
    array_push($adef, rrd::hrule($hw, $_WARNRULE, sprintf("Warning above %.1f°C$nl", $hw)));
    $nl = "";
}
if ($lw != null) {
    array_push($adef, rrd::hrule($lw, $_WARNRULE, sprintf("Warning below %.1f°C$nl", $lw)));
    $nl = "";
}
$def[1] .= join("", array_reverse($adef));

?>
