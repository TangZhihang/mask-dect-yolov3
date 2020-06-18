#训练数据集
log_file=../log/log.txt
python train.py --data-cfg data/rbc.data --cfg cfg/yolov3-tiny.cfg --epochs 100 2>&1 | tee -a ../log/log.txt

#演示数据集
python detect.py --data-cfg data/rbc.data --cfg cfg/yolov3-tiny.cfg --weights ../models/best/best.pt --images ../data/samples 

#测试数据集
python test.py --data-cfg data/rbc.data --cfg cfg/yolov3-tiny.cfg --weights weights/best.pt 
