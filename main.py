from model import ClassificationModel
import argparse
import os


def predict_img(img_path, with_heatmap=False):
    model = ClassificationModel()

    row = model.predict(img_path=img_path, row=None, img=None, load=True, original_image_path=img_path,
                        print_heatmap=with_heatmap)

    results = row.to_json()
    print(results)

    return results


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", help="path of the image", required=True)
    parser.add_argument("--heatmap", "-heat", help="generate heatmap or not", required=True)

    args = parser.parse_args()

    if not(os.path.exists(args.path)):
        raise FileNotFoundError("{} does not exist.".format(args.path))

    elif args.path.split(".")[-1] not in ["png", "jpg", "jpeg"]:
        raise TypeError("The file is not a valid image file.")

    if args.heatmap.upper() == "TRUE":
        args.heatmap = True
    else:
        args.heatmap = False

    result = predict_img(img_path=args.path, with_heatmap=args.heatmap)
