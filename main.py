import sys
import config.chamo
import config.chamo_full_run
import data_preprocessing.default_preprocess
import data_preprocessing.test_preprocess
import net.vgg16
import loss.default_loss
import loss.entropy_loss
import accuracy.default_accuracy
import optimizer.default_opt
import utils.data_helper

config_name=sys.argv[1]
print('choose config: '+config_name)
config_obj=None
if config_name=='chamo':
    config_obj=config.chamo.get_config()
elif config_name=='chamo_full_run':
    config_obj = config.chamo_full_run.get_config()

preprocess_name=config_obj.preprocess_type
preprocess_obj=None
test_preprocess_obj=None
if preprocess_name=='default':
    preprocess_obj=data_preprocessing.default_preprocess.default_preprocess(
        config_obj.tfrecord_test_addr,
        config_obj.batchsize,
        config_obj.class_num
    )

test_preprocess_obj=data_preprocessing.test_preprocess.test_preprocess(config_obj.tfrecord_test_addr, config_obj.class_num)
net_name=config_obj.net_type
net_obj=None
test_net_obj=None
if net_name=='vgg16':
    net_obj=net.vgg16.vgg16(True, 'vgg16', config_obj.class_num)
    test_net_obj=net.vgg16.vgg16(False, 'vgg16', config_obj.class_num)

loss_name=config_obj.loss_type
loss_obj=None
if loss_name=='default':
    loss_obj=loss.default_loss.default_loss()
elif loss_name=='entropy_loss':
    loss_obj =loss.entropy_loss.entropy_loss()

accu_name=config_obj.accuracy_type
accu_obj=None
if accu_name=='default':
    accu_obj=accuracy.default_accuracy.default_accuracy()

opt_name=config_obj.opt_type
opt_obj=None
if opt_name=='default':
    opt_obj=optimizer.default_opt.default_opt(
        config_obj.max_step,
        config_obj.debug_step_len,
        config_obj.result_addr,
        config_obj.stop_accu
    )
images, labels = preprocess_obj.def_preposess()
images_test, labels_test = test_preprocess_obj.def_preposess()
net = net_obj.def_net(images)
net_test = test_net_obj.def_net(images_test)
loss=loss_obj.def_loss(net, labels)
test_accu =accu_obj.def_accuracy(net_test, labels_test)
opt_obj.run(loss, test_accu)
