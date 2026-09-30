# Hand-rolled replacement for what Gradle's packaging step does: take the APK
# aapt2 linked (resources + assets, no code) and add classes.dex to it, keeping
# each entry's compression the way it was (aapt2 stores some entries and
# deflates others, and Android cares).
#
#   python tools/apkzip.py app-unsigned.apk dex-dir out.apk
import os
import sys
import zipfile


def main():
    if len(sys.argv) != 4:
        sys.exit('usage: python tools/apkzip.py <apk> <dexdir> <out.apk>')
    src, dexdir, out = sys.argv[1], sys.argv[2], sys.argv[3]
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(out, 'w') as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            zi = zipfile.ZipInfo(item.filename, date_time=item.date_time)
            zi.compress_type = item.compress_type
            zi.external_attr = item.external_attr
            zi.internal_attr = item.internal_attr
            zi.create_system = item.create_system
            zout.writestr(zi, data)
        for name in sorted(os.listdir(dexdir)):
            if not name.endswith('.dex'):
                continue
            with open(os.path.join(dexdir, name), 'rb') as fh:
                zi = zipfile.ZipInfo(name)          # fixed 1980 stamp: builds stay reproducible
                zi.compress_type = zipfile.ZIP_DEFLATED
                zout.writestr(zi, fh.read())
            print('  +', name)
    print('wrote', out, os.path.getsize(out), 'bytes')


if __name__ == '__main__':
    main()
