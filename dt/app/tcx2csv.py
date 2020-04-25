import re
import xml.etree.ElementTree as et


# takes in a TCX file and outputs a CSV file
def tcx_to_csv (tcx, csv):
    tree = et.ElementTree(et.fromstring(tcx))
    print(tree)
    root = tree.getroot()
    m = re.match(r'^({.*})', root.tag)
    if m:
        ns = m.group(1)
    else:
        ns = ''
    if root.tag != ns+'TrainingCenterDatabase':
        print('Unknown root found: '+root.tag)
        return
    activities = root.find(ns+'Activities')
    if not activities:
        print('Unable to find Activities under root')
        return
    activity=activities.find(ns+'Activity')
    if not activity:
        print('Unable to find Activity under Activities')
        return
    columnsEstablished = False
    for lap in activity.iter(ns+'Lap'):
        if columnsEstablished:
            fout.write('New Lap\n')
        for track in lap.iter(ns+'Track'):
            # pdb.set_trace()
            if columnsEstablished:
                fout.write('New Track\n')
            for trackpoint in track.iter(ns+'Trackpoint'):
                try:
                    time = trackpoint.find(ns+'Time').text.strip()
                except:
                    time = ''
                try:
                    bpm = trackpoint.find(ns+'HeartRateBpm').find(ns+'Value').text.strip()
                except:
                    bpm = ''
                if not columnsEstablished:
                    with open(csv, 'w') as fout:
                        fout.write(','.join(('Time', 'heartratebpm/value'))+'\n')
                        columnsEstablished = True
                        time = time.replace('T', ' ')
                        time = time.replace('Z', '')
                        time = time.replace('.000', '')
                        print(time)
                        print(bpm)
                        fout.write(','.join((time, bpm))+'\n')
                else:
                    with open(csv, 'a') as fout:
                        time = time.replace('T', ' ')
                        time = time.replace('Z', '')
                        time = time.replace('.000', '')
                        print(time)
                        print(bpm)
                        fout.write(','.join((time, bpm)) + '\n')

    fout.close()