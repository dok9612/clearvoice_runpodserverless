from clearvoice import ClearVoice

##-----Use MossFormer2_SR_48K model for speech super-resolution on noisy speech data-----------------
if True:
    # Assume you have noisy speech audios and want to do speech super-resolution
    # Constructs two objects for speech enhancement and super-resolution, respectively.
    myClearVoice_SE = ClearVoice(task='speech_enhancement', model_names=['MossFormer2_SE_48K'])
    myClearVoice_SR = ClearVoice(task='speech_super_resolution', model_names=['MossFormer2_SR_48K'])
    
    # Perform speech enhancement
    output_wav = myClearVoice_SE(input_path='input/test.wav', online_write=False)
    myClearVoice_SE.write(output_wav, output_path='output/test_MossFormer2_SE_48K_input.wav')
    # Perform speech super-resolution
    output_wav = myClearVoice_SR(input_path='output/test_MossFormer2_SE_48K_input.wav', online_write=False)
    myClearVoice_SR.write(output_wav, output_path='output/output_MossFormer2_SR_48K_input.wav')
    
