import os
import imgaug.augmenters as iaa
import cv2

# 데이터 폴더 경로 설정
folder_path = "./Impetigo"  # 이미지 파일들이 있는 폴더 경로를 지정하세요

# 이미지 증강 기법 정의
augmenter = iaa.Sequential([
    iaa.Fliplr(0.5),  # 좌우 반전
    iaa.Affine(rotate=(-10, 10)),  # 회전 (-10도에서 10도 사이)
    iaa.GaussianBlur(sigma=(0, 1.0)),  # 가우시안 블러
    iaa.AdditiveGaussianNoise(scale=(0, 0.05 * 255)),  # 가우시안 노이즈
    iaa.Crop(percent=(0, 0.2))  # 자르기 (0-20% 범위에서)
])

# 폴더 내의 이미지 파일 로드 및 증강
image_files = os.listdir(folder_path)
for image_file in image_files:
    if image_file.endswith((".jpg", ".jpeg", ".png")):
        image_path = os.path.join(folder_path, image_file)
        image = cv2.imread(image_path)

        augmented_images = augmenter(images=[image])

        # 이미지 증강된 결과 저장
        for i, augmented_image in enumerate(augmented_images):
            augmented_file_name = f"augmented_{image_file}_{i}.jpg"
            augmented_file_path = os.path.join(folder_path, augmented_file_name)
            cv2.imwrite(augmented_file_path, augmented_image)
