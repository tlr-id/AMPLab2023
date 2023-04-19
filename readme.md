# Audio Music Processing LAB 2023

3 sub-projects corresponding to this class.

Storing those projects in Git, some work could be done on them :
- Improved comments
- Better formatting & refining the code
- Making the path flexible to any user
- For the Collaborative Filtering task, RAM management can be optimised. Problem has been divided in plenty of small steps and small files.


## 1 - Collaborative Filtering & feature-based playlist generation

#### Collaborative Filtering

Using Listenbrainz's 2022 user data to do a simple collaborative filtering task.

We obtain, for example by quering Mall Grab, the following results :

|   |       artist |    score |
|--:|-------------:|---------:|
| 0 | Mall Grab    | 1.000000 |
| 1 | Overmono     | 0.830906 |
| 2 | DJ Seinfeld  | 0.821291 |
| 3 | DJ Boring    | 0.814272 |
| 4 | Harrison BDP | 0.809491 |
| 5 | Asquith      | 0.805530 |
| 6 | Dax J        | 0.802230 |
| 7 | Riohv        | 0.798247 |
| 8 | Baltra       | 0.795541 |
| 9 | DJ Swagger   | 0.79332  |

/!\ Not usable like this, needs to process a lot of things.
To run just the Implicit model with the right file, just go to this section.

#### Feature-based playlist generation

Based on a dataset of music excerpts, we run several Essentia models to extract data such as Danceability, Music Styles, Arousal ...

Based on this, we design a simple interactive webpage using python's library Streamlit in order to let the user generate playlists.

## 2 - Musicology

This project aimed at carrying a musicologically motivated research task applying music technology methods on non-western music tradition, and to reproduce the whole cycle of conference paper publications.

The paper is untitled ```An exploration of intervallic correlation within Turkish Makam```, and in this paper we classified various Makams based on their intervallic progression. For this, we used simple classifications algorithms, and with this approach, we easily obtained state of the art-level results for this task (87% in `Classification of turkish makam music: a topological approach`) .

This paper was nominated for the "award-winning quality" of the class.

## 3 - Audio Mosaicing using Freesound

This project consisted in recreating a given song from fragments of other sounds retrieved using Freesound.

A bank of fragments is created and analyzed using Essentia, and for a fragment of the original song, the closest fragment in the bank replaces this one.

Applied for 2 tracks with more or less success :
- Midnight on Rainbow Road by Leon Vynehall (drone-y track)
- Can You Float by Sidewinder (aka D.Dan) (high speed transe-y track)