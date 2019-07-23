import os
from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image

from tf_explain.utils.display import filter_display


class ExtractActivations:

    """ Draw activations of a specific layer for a given input """

    def explain(self, validation_data, model, layers_name):
        outputs = [
            layer.output for layer in model.layers
            if layer.name in layers_name
        ]

        activations_model = tf.keras.models.Model(model.inputs, outputs=outputs)
        activations_model.compile(optimizer="sgd", loss="categorical_crossentropy")

        predictions = activations_model.predict(validation_data[0])
        grid = filter_display(predictions)

        return grid

    def save(self, grid, output_dir, output_name):
        os.makedirs(output_dir, exist_ok=True)

        grid_as_image = Image.fromarray((np.clip(grid, 0, 1) * 255).astype("uint8"))
        grid_as_image.save(Path(output_dir) / output_name)
