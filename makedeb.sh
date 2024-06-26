#!/bin/bash

PACKAGE=prucam-pirt1280
DATE=`date "+%a, %d %b %Y %T %z"`
VERSION=`git describe --tags --abbrev=0`
VERSION="${VERSION:1}"  # remove leading 'v'

cat > "debian/changelog" <<-__EOF__
$PACKAGE ($VERSION-0) buster; urgency=low

  * See git logs at https://github.com/oresat/oresat-linux-prucam/releases

 -- PSAS <oresat@pdx.edu>  $DATE
__EOF__

dpkg-buildpackage -us -uc

mv ../$PACKAGE*.deb .
rm -f ../$PACKAGE*
