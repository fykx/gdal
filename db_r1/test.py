from fykx.fmath import ConfusionMatrix
from fykx.fmath import RmseMae


def main():
    data = r'/mnt/e/r1/out/csv/result_3.csv'
    weight = -1
    predicted = 2
    actual = -3
    prob = 5

    pathout = r'/mnt/e/r1/out/csv'

    nn = pathout + '/' + 'result_4_loss.csv'
    f = open(nn, 'w')

    f.write('{},{},{},{},{},{}\n'.format('thr','overall_accuracy','pro_accuracy_true','pro_accuracy_false','user_accuracy_true','user_accuracy_false'))

    thr = 0
    while thr <= 100:
        c = ConfusionMatrix(data, weight, predicted, actual, prob, thr)
        f.write('{},{},{},{},{},{}\n'.format(thr,c.overall_accuracy(),c.pro_accuracy_true(),c.pro_accuracy_false(),c.user_accuracy_true(),c.user_accuracy_false()))
        thr = thr + 1


    #rm = RmseMae(data, predicted, actual)
    #print('RMSE:', rm.root_mean_square_error())
    #print('MAE:', rm.mean_absolute_error())
    return


if __name__ == '__main__':
    main()

