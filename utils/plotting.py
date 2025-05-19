import os


def plotme(plt_, plot_id, plot_name, plot_path='plots', show_flag=True, ignore_eps=True, pad_inches=0):
    if show_flag:
        print('Showing Plot {}-{}'.format(plot_id, plot_name))
        plt_.show(bbox_inches='tight')
    else:
        ax = plt_.gca()
        os.makedirs(os.path.join(plot_path, 'png'), exist_ok=True)
        os.makedirs(os.path.join(plot_path, 'pdf'), exist_ok=True)

        plt_.savefig(os.path.join(plot_path, 'png', f'{plot_id}-{plot_name}.png'), format='png', dpi=300,
                     bbox_inches='tight', pad_inches=pad_inches)
        plt_.savefig(os.path.join(plot_path, 'pdf', f'{plot_id}-{plot_name}.pdf'), format='pdf', dpi=300,
                     bbox_inches='tight', pad_inches=pad_inches)
        if not ignore_eps:
            # Save it with rasterized points
            ax.set_rasterization_zorder(1)
            os.makedirs(os.path.join(plot_path, 'eps'), exist_ok=True)
            plt_.savefig(os.path.join(plot_path, 'eps', f'{plot_id}-{plot_name}.eps'), dpi=300, rasterized=True,
                         bbox_inches='tight', pad_inches=0)
        print('Saved Plot {}-{}'.format(plot_id, plot_name))
