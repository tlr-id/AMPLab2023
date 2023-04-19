import os.path
import random
import streamlit as st
import pandas
import ast


m3u_filepaths_file = 'playlists/streamlit.m3u8'
ESSENTIA_ANALYSIS_PATH = './feature_extracted_final_better_formated.pickle'

def load_essentia_analysis():
    return pandas.read_pickle(ESSENTIA_ANALYSIS_PATH)

st.write('# Audio analysis playlists')
st.write(f'Using analysis data from `{ESSENTIA_ANALYSIS_PATH}`.')
audio_analysis = load_essentia_analysis()
audio_analysis_styles = audio_analysis.columns[-400:]
st.write('Loaded audio analysis for', len(audio_analysis), 'tracks.')

st.write('## 🔍 Select')

st.write('### By style')
st.write('Style activation statistics:')
st.write(audio_analysis.describe())

style_select = st.multiselect('Select by style activations:', audio_analysis_styles)

if style_select:
    # Show the distribution of activation values for the selected styles.
    st.write(audio_analysis[style_select].describe())

    style_select_str = ', '.join(style_select)
    style_select_range = st.slider(f'Select tracks with `{style_select_str}` activations within range:', value=[0.5, 1.])

### Adding Tempo slider
st.write('## By tempo')
st.write('Select the tempo range:')
min_tempo = min(audio_analysis['bpm'][:])
max_tempo = max(audio_analysis['bpm'][:])
tempo_slider = st.slider('Tempo', min_tempo, max_tempo,(min_tempo,max_tempo))

### Voice/Instru : binary classif
st.write('## Vocal and/or Instru ?')
st.write('Make a choice:')
voice_instru_radio = st.radio("Pick one",['Both','Voice', 'Instru'])

### Danceability slider
st.write('## By Danceability')
st.write('Select a value range:')
min_dance = min(audio_analysis['danceability'][:])
max_dance = max(audio_analysis['danceability'][:])
danceability_slider = st.slider('Danceability',min_dance,max_dance,(min_dance,max_dance))

### Arousal & Valence sliders
st.write('## By Arousal/Valence')
st.write('Select ranges:')
min_val = min(audio_analysis['valence'][:])
max_val = max(audio_analysis['valence'][:])
min_aro = min(audio_analysis['arousal'][:])
max_aro = max(audio_analysis['arousal'][:])
valence_slider = st.slider('Valence',min_val,max_val,(min_val,max_val))
arousal_slider = st.slider('Arousal',min_aro,max_aro,(min_aro,max_aro))

st.write('## 🔝 Rank')
style_rank = st.multiselect('Rank by style activations (multiplies activations for selected styles):', audio_analysis_styles, [])

st.write('## 🔀 Post-process')
max_tracks = st.number_input('Maximum number of tracks (0 for all):', value=0)
shuffle = st.checkbox('Random shuffle')

if st.button("RUN"):
    st.write('## 🔊 Results')

    mp3s = list(audio_analysis.index)
    
    audio_analysis_query = audio_analysis.loc[mp3s][style_select]

    result = audio_analysis_query
    for style in style_select:
        result = result.loc[result[style] >= style_select_range[0]]
    mp3s = result.index
    
    if style_rank:
        audio_analysis_query = audio_analysis.loc[mp3s][style_rank]
        audio_analysis_query['RANK'] = audio_analysis_query[style_rank[0]]
        for style in style_rank[1:]:
            audio_analysis_query['RANK'] *= audio_analysis_query[style]
        ranked = audio_analysis_query.sort_values(['RANK'], ascending=[False])
        ranked = ranked[['RANK'] + style_rank]
        mp3s = list(ranked.index)

        st.write('Applied ranking by audio style predictions.')
        st.write(ranked)

    if max_tracks:
        mp3s = mp3s[:max_tracks]
        st.write('Using top', len(mp3s), 'tracks from the results.')

    if shuffle:
        random.shuffle(mp3s)
        st.write('Applied random shuffle.')

    mp3_final = []
    
    # Filtering everything
    for mp3 in mp3s:

        # Tempo
        if audio_analysis['bpm'][mp3] >= tempo_slider[0] and audio_analysis['bpm'][mp3] <= tempo_slider[1]:

            # Danceability
            if audio_analysis['danceability'][mp3] >= danceability_slider[0] and audio_analysis['danceability'][mp3] <= danceability_slider[1]:

                # valence
                if audio_analysis['valence'][mp3] >= valence_slider[0] and audio_analysis['valence'][mp3] <= valence_slider[1]:
                        
                    if audio_analysis['arousal'][mp3] >= arousal_slider[0] and audio_analysis['arousal'][mp3] <= arousal_slider[1]:

                        # Vocal / Instru /!\ it's mixed in our csv file
                        if voice_instru_radio == 'Voice':# choix user vocal :
                            if audio_analysis['voice'][mp3] <= audio_analysis['instru'][mp3]:
                                mp3_final.append(mp3)

                        elif voice_instru_radio == 'Instru':# choix user vocal
                            if audio_analysis['instru'][mp3] <= audio_analysis['voice'][mp3]:
                                mp3_final.append(mp3)

                        else:
                            mp3_final.append(mp3)

    audio_analysis_query = audio_analysis.loc[mp3_final]
    result = audio_analysis_query

    st.write(result)


    # Store the M3U8 playlist.
    with open(m3u_filepaths_file, 'w') as f:
        # Modify relative mp3 paths to make them accessible from the playlist folder.
        mp3_paths = [os.path.join('..', audio_analysis['fullpath'][mp3]) for mp3 in mp3_final]
        f.write('\n'.join(mp3_paths))
        st.write(f'Stored M3U playlist (local filepaths) to `{m3u_filepaths_file}`.')

    st.write('Audio previews for the first 10 results:')
    for mp3 in mp3_final[:10]:
        st.audio(f'./{audio_analysis["fullpath"][mp3]}', format="audio/mp3", start_time=0)
