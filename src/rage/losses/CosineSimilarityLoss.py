from typing import Iterable, Dict
import torch 
from torch import nn, Tensor
from .loss_rag import LossRAG
from ..constant import EMBEDDING_RANKER_NUMERICAL

class CosineSimilarityLoss(LossRAG): 
    def __init__(self, loss_fct= nn.MSELoss(), cos_score_transformation= nn.Identity()): 
        super(CosineSimilarityLoss, self).__init__()
        self.loss_fct= loss_fct
        self.cos_score_transformation= cos_score_transformation
        
        self.pretty_name= "cosine_similarity"
        self.task_name= EMBEDDING_RANKER_NUMERICAL
    
    def _get_config_params(self):
        return {
            'pretty_name': self.pretty_name, 
            'task_name': self.task_name
        }
    
    
    def forward(self, features: Iterable[Dict[str, Tensor]], labels: Tensor): 
        embeddings= self.model(features, return_embeddings= True)

        output= self.cos_score_transformation(torch.cosine_similarity(embeddings[0], embeddings[1]))
        return self.loss_fct(output.view(-1,), labels.view(-1).to(dtype= torch.float32))