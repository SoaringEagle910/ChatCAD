import numpy as np
import torch
import torch.nn as nn

from r2g.modules.base_cmn import BaseCMN
from r2g.modules.visual_extractor import VisualExtractor


class BaseCMNModel(nn.Module):
    def __init__(self, cfg, tokenizer):
        super(BaseCMNModel, self).__init__()
        # self.args = args
        self.tokenizer = tokenizer
        self.visual_extractor = VisualExtractor(cfg)
        self.encoder_decoder = BaseCMN(cfg, tokenizer)
        # if args.dataset_name == 'iu_xray':
        #     self.forward = self.forward_iu_xray
        # else:
        self.forward = self.forward_mimic_cxr

    def __str__(self):
        model_parameters = filter(lambda p: p.requires_grad, self.parameters())
        params = sum([np.prod(p.size()) for p in model_parameters])
        return super().__str__() + '\nTrainable parameters: {}'.format(params)

    def forward_iu_xray(self, images, targets=None, mode='train', update_opts={}):
        print(11111)
        att_feats_0, fc_feats_0 = self.visual_extractor(images[:, 0])
        print(12222)
        att_feats_1, fc_feats_1 = self.visual_extractor(images[:, 1])
        print(13333)
        fc_feats = torch.cat((fc_feats_0, fc_feats_1), dim=1)
        print(14444)
        att_feats = torch.cat((att_feats_0, att_feats_1), dim=1)
        print(15555)
        print("mode:")
        print(mode)
        if mode == 'train':
            output = self.encoder_decoder(fc_feats, att_feats, targets, mode='forward')
            return output
        elif mode == 'sample':
            output, output_probs = self.encoder_decoder(fc_feats, att_feats, mode='sample', update_opts=update_opts)
            print(16666)
            return output, output_probs
        else:
            raise ValueError

    def forward_mimic_cxr(self, images, targets=None, mode='train', update_opts={}):
        print(21111)
        att_feats, fc_feats = self.visual_extractor(images)
        print(22222)
        print("mode:")
        print(mode)
        if mode == 'train':
            output = self.encoder_decoder(fc_feats, att_feats, targets, mode='forward')
            return output
        elif mode == 'sample':
            output, output_probs = self.encoder_decoder(fc_feats, att_feats, mode='sample', update_opts=update_opts)
            print(23333)
            return output, output_probs
        else:
            raise ValueError
