from enum import Enum

import torch
import torch.nn as nn
from django.conf import settings
from transformers import BertModel, BertTokenizer

from decorators.log_decorators import log_function


class OperationResult(Enum):
    SUCCESS = 1
    FAILURE = 2
    MODEL_ALREADY_LOADED = 3


class BERTGRUSentiment(nn.Module):
    def __init__(self, bert, hidden_dim, output_dim, num_layers, bidirectional, dropout):
        super().__init__()
        self.bert = bert
        for param in self.bert.parameters():
            param.requires_grad = False
        embedding_dim = bert.config.to_dict()['hidden_size']
        self.rnn = nn.GRU(
            input_size=embedding_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            bidirectional=bidirectional,
            batch_first=True,
            dropout=0 if num_layers < 2 else dropout
        )
        self.out = nn.Linear(hidden_dim * 2 if bidirectional else hidden_dim, output_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, input_ids, attention_mask):
        with torch.no_grad():
            embedded = self.bert(input_ids=input_ids, attention_mask=attention_mask)[0]
        if torch.isnan(embedded).any():
            raise ValueError("NaN values detected in BERT embeddings")
        _, hidden = self.rnn(embedded)
        if torch.isnan(hidden).any():
            raise ValueError("NaN values detected in GRU hidden states")
        if self.rnn.bidirectional:
            hidden = self.dropout(torch.cat((hidden[-2, :, :], hidden[-1, :, :]), dim=1))
        else:
            hidden = hidden[-1, :, :]
        if torch.isnan(hidden).any():
            raise ValueError("NaN values detected after dropout")
        output = self.out(hidden)
        if torch.isnan(output).any():
            raise ValueError("NaN values detected in output")
        return output


class ToxicityModelInterface:
    _model = None
    _device = None
    _bert_model = BertModel.from_pretrained('bert-base-uncased')
    _tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    @classmethod
    @log_function
    def load_model(cls, device='cpu'):
        if cls._model is None:
            try:
                cls._device = device
                cls._model = BERTGRUSentiment(cls._bert_model, 256, 1, 4, True, 0.1).to(cls._device)
                cls._model.load_state_dict(torch.load(str(settings.MODELS_ROOT / 'toxicity_model.pth')))
                cls._model.eval()
                return OperationResult.SUCCESS
            except:
                return OperationResult.FAILURE
        else:
            return OperationResult.MODEL_ALREADY_LOADED

    @classmethod
    @log_function(log_result=False)
    def predict_toxicity(cls, text, threshold=0.5):
        cls._model.eval()
        max_input_length = cls._tokenizer.max_model_input_sizes['bert-base-uncased']

        encoded_dict = cls._tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            truncation=True,
            max_length=max_input_length,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt',
        )

        input_ids = encoded_dict['input_ids'].to(cls._device)
        attention_mask = encoded_dict['attention_mask'].to(cls._device)

        with torch.no_grad():
            outputs = cls._model(input_ids, attention_mask)

        prediction = torch.sigmoid(outputs).item()
        is_toxic = prediction > threshold

        return is_toxic

    @classmethod
    @log_function(log_result=False)
    def is_loaded(cls):
        if isinstance(cls._model, BERTGRUSentiment):
            return True
        else:
            return False
