import json
from typing import List, Optional

from mlp_sdk.abstract import Task
from mlp_sdk.grpc import mlp_grpc_pb2
from mlp_sdk.hosting.host import host_mlp_cloud
from mlp_sdk.transport.MlpServiceSDK import MlpServiceSDK
from mlp_sdk.transport.MlpClientSDK import MlpRestClient, MlpClientSDK
from pydantic import BaseModel


class TextsCollection(BaseModel):
    texts: List[str]


ACCOUNT = "just-ai"
GRAMMAR_SERVICE = "spellcheck"
PUNCTUATION_SERVICE = "punctuation"


class CompositeActionExample(Task):

    def __init__(self, config: BaseModel, service_sdk: MlpServiceSDK = None) -> None:
        super().__init__(config, service_sdk)
        self.client = MlpClientSDK()
        self.client.init()

    def get_descriptor(self):
        return mlp_grpc_pb2.ServiceDescriptorProto(
            name="example",
            fittable=False,
            methods={"predict": mlp_grpc_pb2.MethodDescriptorProto(
                input={"data": mlp_grpc_pb2.ParamDescriptorProto(type="TextsCollection")},
                output=mlp_grpc_pb2.ParamDescriptorProto(type="TextsCollection"),
            )
            }
        )

    def predict(self, data: TextsCollection, config=None) -> TextsCollection:
        corrected_texts = self.__correct_texts(data)

        return self.__punctuate_texts(corrected_texts)

    def __correct_texts(self, texts: TextsCollection) -> TextsCollection:
        res = self.client.predict(ACCOUNT, GRAMMAR_SERVICE, texts.json())
        response_json = res.data.json

        corrected_texts_list = json.loads(response_json)["corrected_texts"]
        return TextsCollection(texts=corrected_texts_list)

    def __punctuate_texts(self, texts: TextsCollection) -> TextsCollection:
        res = self.client.predict(ACCOUNT, PUNCTUATION_SERVICE, texts.json())
        response_json = res.data.json

        punctuated_texts_list = json.loads(response_json)["texts"]
        return TextsCollection(texts=punctuated_texts_list)


if __name__ == "__main__":
    host_mlp_cloud(CompositeActionExample, BaseModel())
