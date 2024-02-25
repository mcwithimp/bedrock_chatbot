import json
import logging
import os
import base64
import random
import boto3

# 로깅 설정을 초기화함
logging.basicConfig(level=logging.INFO)

class ImageGenerator:
    def __init__(self):
        # Amazon Bedrock Runtime 클라이언트를 초기화함
        self.client = boto3.client('bedrock-runtime', region_name='us-east-1')

    def generate_image(self, prompt):
        # 이미지 생성을 위한 난수 시드를 생성함
        seed = random.randint(0, 2147483647)
        # 이미지 생성 요청 데이터를 구성함
        request_data = {
            "taskType": "TEXT_IMAGE", "textToImageParams": {"text": prompt},
            "imageGenerationConfig": {
                "numberOfImages": 1, "quality": "standard", "cfgScale": 7.5,
                "height": 512, "width": 512, "seed": seed,
            }
        }
        try:
            # 모델을 호출하여 이미지를 생성함
            response = self.client.invoke_model(
                modelId="amazon.titan-image-generator-v1", body=json.dumps(request_data))
            # 응답에서 base64 인코딩된 이미지 데이터를 추출함
            base64_image_data = json.loads(response["body"].read())["images"][0]
            # 추출된 이미지 데이터를 파일로 저장함
            return self.save_image(base64_image_data, prompt)
        except Exception as e:
            # 이미지 생성 중 오류가 발생하면 로깅함
            logging.error(f"이미지 생성 중 오류 발생: {e}")
            raise

    def save_image(self, base64_image_data, prompt):
        # 이미지를 저장할 폴더를 생성함(이미 존재하면 생성하지 않음)
        output_folder = 'generated_images'
        os.makedirs(output_folder, exist_ok=True)
        # 저장할 이미지 파일의 경로를 생성함
        file_path = os.path.join(output_folder, f"{prompt}_{random.randint(1000, 9999)}.png")
        # base64 인코딩된 데이터를 이미지 파일로 변환하여 저장함
        with open(file_path, 'wb') as file:
            file.write(base64.b64decode(base64_image_data))
        # 이미지 저장 경로를 로깅함
        logging.info(f"이미지 저장됨: {file_path}")
        return file_path

def main():
    # 이미지 생성 작업을 시작함
    logging.info("Amazon Bedrock 이미지 생성 시작")
    # 이미지 생성기 인스턴스를 생성함
    generator = ImageGenerator()
    # 이미지 생성을 위한 텍스트 프롬프트 설정
    prompt = "Golden Retriever scuba diving in the deep sea wearing a mask and flippers"
    # 이미지를 생성하고 그 경로를 반환
    image_path = generator.generate_image(prompt)
    logging.info(f"생성된 이미지 경로: {image_path}")

if __name__ == "__main__":
    main()
