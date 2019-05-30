from pixelation import TypePixelation, Pixelation

pixelation = Pixelation('res/hard.jpg', 10, 100, TypePixelation.NEURAL_NETWORK)
pixelation.process_image()

pixelation = Pixelation('res/hard.jpg', 10, 100, TypePixelation.K_AVERAGE_RANDOM_POINT)
pixelation.process_image()
