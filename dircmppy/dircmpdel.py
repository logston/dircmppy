import os
import errno


def delete_file(file_name, dry=False):
    if dry:
        print('    DRY DELETED: {}'.format(file_name))
    else:
        os.remove(file_name)
        try:
            dirname = os.path.dirname(file_name)
            os.rmdir(dirname)
            print('    DELETED DIR: {}'.format(dirname))
        except OSError as ex:
            if ex.errno != errno.ENOTEMPTY:
                raise
        print('    DELETED: {}'.format(file_name))


def run_dircmpdel(dircmp_file, prompt=True, dry=False):
    """
    Parse dircmp file for groups of file names to be deleted.
    """
    with open(dircmp_file) as fp:
        lines = fp.read()
    groups = lines.strip().split('\n\n')
    print('Found {} duplicate groups'.format(len(groups)))

    groups = (group.split('\n') for group in groups)
    checked_proper_cwd = False
    for group in groups:
        for i, file_name in enumerate(group):
            if not i:
                if not checked_proper_cwd:
                    if not os.path.exists(file_name):
                        raise RuntimeError('File {} could not be found. '
                                           'Please ensure you are in the '
                                           'correct directory.'
                                           ''.format(file_name))
                    checked_proper_cwd = True
                print('Deleting duplicates of {}'.format(file_name))
            else:
                if prompt:
                    while True:
                        resp = input('    Delete {}? '.format(file_name))
                        resp = resp.lower()
                        if resp not in ('yes', 'no'):
                            print('Please answer "yes" or "no".')
                        elif resp == 'yes':
                            delete_file(file_name, dry=dry)
                            break
                        elif resp == 'no':
                            print('    Not deleted: {}'.format(file_name))
                            break
                else:
                    delete_file(file_name, dry=dry)
        print()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Utility for deleting duplicate files found by dircmp'
    )
    parser.add_argument('file')
    parser.add_argument('--no-prompt', 
                        action='store_false', default=True, dest='prompt')
    parser.add_argument('-d', '--dry',
                        action='store_true', default=False, dest='dry')
    args = parser.parse_args()

    run_dircmpdel(args.file, prompt=args.prompt, dry=args.dry)

