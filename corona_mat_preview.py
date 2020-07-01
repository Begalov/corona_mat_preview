# Script demonstrate bug with standalone corona renderer v5 from the kit for 3ds max
# by generating few images with different size where the sphere is shifted up.

# Change to Corona path:
corona_path = "C:\\Program Files\\Corona\\Corona Renderer for 3ds Max\\Standalone\\Corona.exe"

import os, subprocess, sys, datetime
corona_proc = None


def debug( *args):
    msg = ' '.join(['%s'%a for a in args])
    print( "debug:  ", msg)


def gatherOutput(proc, startup, until, showOutput = True):
    buf = ''
    while proc.poll() == None:
        data = proc.stdout.read(1)
        buf += data
        if showOutput:
            sys.stdout.write(data)
            sys.stdout.flush()
        if buf == until or data == '\n':
            if buf == until:
                return True
            else:
                buf = ''
    return False


def kill_preview():
    global corona_proc
    if corona_proc and corona_proc.poll() == None:
        corona_proc.terminate()


def render_preview():
    global corona_path, corona_proc

    dims = (
        (32, 32),
        (32*2, 32),
        (32, 32*2),
        (32*8, 32*16),
        (32*16, 32*8),
        )

    tempdir = os.getcwd()
    output_path = os.path.join(tempdir + '\\preview\\')
    if not os.path.isdir( output_path):
        os.makedirs( output_path, exist_ok = True)

    startup = False
    # Start the preview process if it isn't running
    if corona_proc == None or corona_proc.poll() != None:
        debug("Starting preview process")
        cmd = ( corona_path, '-mtlPreview')
        startup = True
        corona_proc = subprocess.Popen(cmd,
            stderr = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stdin = subprocess.PIPE,
            shell = (os.name != 'posix'),
            cwd = output_path,
            bufsize = 1,
            universal_newlines = True)
        gatherOutput(corona_proc, startup, '\n')
        debug("Ready to render previews")
        startup = False

    for d in dims:
        output_file = os.path.join( output_path, "matpreview_%dx%d.jpg" % (d[0], d[1])) #int(uid)
        preview_quality = 1
        material = '<material class="Native"><diffuse>0.15 0.05 0.78</diffuse></material>'
        exporter = "%d %d %s " % ( d[0], d[1], output_file)
        exporter += material + '\0'
        # This is the real preview render
        corona_proc.stdin.write('%.3f %s' % (preview_quality, exporter))
        corona_proc.stdin.flush()
        gatherOutput(corona_proc, startup, '.', showOutput = False) #False

    kill_preview()


render_preview()