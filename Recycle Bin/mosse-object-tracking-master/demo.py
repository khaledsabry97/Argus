from mosse import mosse
import argparse

parse = argparse.ArgumentParser()
parse.add_argument('--lr', type=float, default=0.025, help='the learning rate')
parse.add_argument('--sigma', type=float, default=30, help='the sigma')
parse.add_argument('--num_pretrain', type=int, default=1028, help='the number of pretrain')
parse.add_argument('--rotate', action='store_true', help='if rotate image during pre-training.')
parse.add_argument('--record', action='store_true', help='record the frames')

if __name__ == '__main__':
    args = parse.parse_args()
    # img_path = 'datasets/surfer/'
    img_path = 'datasets/1544/'

    tracker = mosse(args, img_path)
    tracker.start_tracking()
