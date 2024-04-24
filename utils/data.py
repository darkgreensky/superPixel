class Data:
    img_label = []
    have_img_label = False
    have_segmented_img = False
    segmented_img = None
    height = 0
    width = 0
    use_algorithm = None
    num_superpixels = 0
    img_type = 0
    """
    0 表示图片信息是打开图片计算的
    1 表示图片信息是打开的数据文件
    """

    human_label = []
    have_human_label = False
    human_num_superpixels = 0
    have_human_segmented_img = False
    human_segmented_img = None

    _observers = []

    @staticmethod
    def set_have_img_label_handle(have_img_label):
        if not Data.have_img_label:
            Data.notify_observers(have_img_label)
            Data.have_img_label = have_img_label

    @staticmethod
    def add_observer(observer):
        Data._observers.append(observer)

    @staticmethod
    def remove_observer(observer):
        Data._observers.remove(observer)

    @staticmethod
    def notify_observers(value):
        for observer in Data._observers:
            observer.update(value)

    @staticmethod
    def update_img_info(img_label=None, num_superpixels=0, img_type=0, have_img_label=True, segmented_img=None,
                        height=0, width=0, use_algorithm=''):
        if img_label is not None:
            Data.img_label = img_label
        Data.num_superpixels = num_superpixels
        Data.img_type = img_type
        Data.set_have_img_label_handle(have_img_label)
        if segmented_img is not None:
            Data.segmented_img = segmented_img
            Data.have_segmented_img = True
        if height:
            Data.height = height
        if width:
            Data.width = width
        # if use_algorithm != '':
        Data.use_algorithm = use_algorithm

    @staticmethod
    def update_human_img_info(img_label, num_superpixels: int, have_img_label: bool, segmented_img=None):
        Data.human_label = img_label
        Data.human_num_superpixels = num_superpixels
        Data.have_human_label = have_img_label
        if segmented_img is None:
            Data.have_human_segmented_img = False
        else:
            Data.human_segmented_img = segmented_img
            Data.have_human_segmented_img = True
