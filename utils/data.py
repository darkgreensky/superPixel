class Data:
    img_label = []
    have_img_label = False
    num_superpixels = 0
    have_segmented_img = False
    segmented_img = None

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
        print(observer)

    @staticmethod
    def remove_observer(observer):
        Data._observers.remove(observer)

    @staticmethod
    def notify_observers(value):
        for observer in Data._observers:
            observer.update(value)

    @staticmethod
    def update_img_info(img_label, num_superpixels: int, have_img_label: bool, segmented_img=None):
        Data.img_label = img_label
        Data.num_superpixels = num_superpixels
        Data.set_have_img_label_handle(have_img_label)
        if segmented_img is None:
            Data.have_segmented_img = False
        else:
            Data.segmented_img = segmented_img
            Data.have_segmented_img = True

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
