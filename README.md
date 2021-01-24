# ngram-rhapsody 複製語撚

用[〈絮言・狂想〉podcast](https://www.rhapsodyinlingo.com/jyut/收聽/) 嘅逐字稿訓練成嘅 trigram language model gen 出嚟嘅嘢，因爲講啲嘢好語言向，所以叫複製語撚（擺明個名係抄[複製陳雲](https://www.youtube.com/watch?v=m-kgJ00cl5o)）。

## 運作原理

一個 language model（LM）嘅作用就係根據一句嘢之前見到嘅字，推測下一個字係乜嘢，而 n-gram 係其中一種 LM。例如如果你望下 `rhapsody-lm-7` 呢個 file，你會見到每行有三個字元，然後後面有一個 0 至 1 嘅數字。譬如第五行寫住 `一個好	0.06686478454680535`，即係話「好」出現喺「一個」後面嘅機率係大概 0.067。

所以每行嘅數字就係第三個字元出現喺頭兩個字元後面嘅機率，因爲係每三個字元噉計，所以呢個叫 trigram model（n=3 嘅 n-gram）。

呢個 model 係好簡單嘅 maximum likelihood estimation，即係純粹係計晒原稿裏面所有三個字元組合嘅數量，然後再除返總數。例如文中有 100 個 `ab`，有 90 個 `ab` 後面係 `c`，其餘 10 個 `ab` 後面係 `d`，噉 `abc` 同 `abd` 嘅機率就會係 0.9 同 0.1。

所以佢只係識 gen 一啲佢已經見過嘅嘢，而且因爲 trigram model gen 每一個字元只會參考前兩個字元，所以出到嚟係會九唔搭八，要參考更長嘅 history 就要多啲 data 喇（）。

## 點用？
如果你用 macOS/Linux，可以首先裝 Python 3，然後用 command line，去返 main.py 個路徑：

`cd .../ngram-rhapsody` ← 改返做啱嘅 path

### 訓練 LM

想訓練一個 LM，可以 run 呢句：

`python3 main.py train script.txt rhapsody-lm`

`script.txt` 可以改做你想要嘅另一個 .txt file，呢個應該係未經處理嘅文稿，`rhapsody-lm` 係你想 train 咗出嚟個 model 嘅名

### 生成語撚！

有咗 language model 之後，就可以生成語撚喇！只需要去返啲 file 嘅路徑，然後打：

`python3 main.py generate rhapsody-lm`

同樣，可以將 `rhapsody-lm` 改成你想用嚟 gen 嘢嗰個 model
