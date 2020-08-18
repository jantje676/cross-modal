from train import start_experiment
import argparse
from utils import find_run_name, set_run_name
import tb as tb_logger
import logging

def main(opt):
    nr_runs = opt.nr_runs
    seeds = [opt.seed1, 4, 26]

    # find run name and set to seed1
    nr_next_run = find_run_name(opt)

    for i in range(nr_runs):
        opt = set_run_name(opt, nr_next_run, i+1)
        logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
        tb_logger.configure(opt.logger_name, flush_secs=5)


        start_experiment(opt, seeds[i])



if __name__ == '__main__':
    # Hyper Parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', default='../data',
                        help='path to datasets')
    parser.add_argument('--clothing', default='dresses',
                        help='which clothing item')
    parser.add_argument('--data_name', default='Fashion200K',
                        help='{coco,f30k}_precomp')
    parser.add_argument('--vocab_path', default='../vocab',
                        help='Path to saved vocabulary json files.')
    parser.add_argument('--margin', default=40., type=float,
                        help='Rank loss margin.')
    parser.add_argument('--num_epochs', default=20, type=int, help='Number of training epochs.')
    parser.add_argument('--n', default=10, type=int, help='smoothing term')
    parser.add_argument('--switch', default=15, type=int, help='switch objective function after n-epochs')
    parser.add_argument('--batch_size', default=128, type=int,
                        help='Size of a training mini-batch.')
    parser.add_argument('--word_dim', default=300, type=int,
                        help='Dimensionality of the word embedding.')
    parser.add_argument('--embed_size', default=1024, type=int,
                        help='Dimensionality of the joint embedding.')
    parser.add_argument('--num_layers', default=1, type=int,
                        help='Number of GRU layers.')
    parser.add_argument('--learning_rate', default=.00001, type=float,
                        help='Initial learning rate.')

    parser.add_argument('--alpha', default=.25, type=float,
                        help='alpha weight decay')
    parser.add_argument('--beta', default=.5, type=float,
                        help='beta global weight')
    parser.add_argument('--gamma', default=.5, type=float,
                        help='gamma weight for k-means objective')
    parser.add_argument('--workers', default=10, type=int,
                        help='Number of data loader workers.')
    parser.add_argument('--log_step', default=10, type=int,
                        help='Number of steps to print and record the log.')
    parser.add_argument('--val_step', default=2000, type=int,
                        help='Number of steps to run validation.')
    parser.add_argument('--logger_name', default='./runs/run0/log',
                        help='Path to save Tensorboard log.')
    parser.add_argument('--model_name', default='./runs/run0/checkpoint',
                        help='Path to save the model.')
    parser.add_argument('--resume', default='', type=str, metavar='PATH',
                        help='path to latest checkpoint (default: none)')
    parser.add_argument('--img_dim', default=4096, type=int,
                        help='Dimensionality of the image embedding.')
    parser.add_argument('--bi_gru', action='store_true',
                        help='Use bidirectional GRU.')
    parser.add_argument('--version', default="laenen", type=str,
                        help='version.')
    parser.add_argument('--nr_runs', default=1, type=int,
                        help='Number of experiments.')
    parser.add_argument('--seed1', default=17, type=int,
                        help='first seed to change easily')
    parser.add_argument('--shard_size', default=128, type=int,
                        help='shard size')
    parser.add_argument('--n_clusters', default=5000, type=int,
                        help='number of clusters for kmeans')
    parser.add_argument('--cluster_loss', action='store_true',
                        help='use of third loss component: image cluster loss')




    opt = parser.parse_args()
    main(opt)