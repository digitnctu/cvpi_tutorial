====
目標
====

---------------------
case1 驅動程式界面
---------------------

在這個案例中，驗證程式提供的驅動程式界面。從架構圖來看 arch_ ，驅動程式放在librw.so裏；而驗證程式libreg.so實現了讀/寫驅動時序如 wave_ ； reg_if是我們要驗證的DUT，被放在top模組內。libpattern.so註冊我們的VPI function $hello，提供了我們驗證程式的進入點，同時結合libreg.so以及librw.so來提供驗證功能。

當在DUT呼叫$hello時，驗證程式會啟動執行緒並在此執行緒呼叫在librw.so中entry_point函數，等待驅動程式呼叫實現於libreg.so的issue_r/issue_w函數。

..
	這個項目是SW/HW同時模擬的例子。SW透過函數對HW(reg_if)讀寫。根據 arch_ 可以了解：SW的一系列讀寫程序寫在entry_point的函數內編譯成共享程式庫(shared-library)librw.so，使用程式將entry_point當作SW的進入點。上述的讀寫函數是由libreg.so這個程式連所提供。在這些函數中，libreg.so將利用CVPI所提供的工具實現 wave_ 的讀寫時序，以完成和HW(reg_if)溝通的目的。
	
.. _wave:

..
	marker

.. wavedrom::

	{ "signal" : [
		 { "wave":"p.......", "name":"clk",
		   "node":"........", "data":[]
		}
		,[ "input"
		,{ "wave":"01.01.0.", "name":"cs",
		   "node":"........", "data":[]
		}
		,{ "wave":"01.0....", "name":"wr",
		   "node":"........", "data":[]
		}
		,{ "wave":"22.22.2.", "name":"adr",
		   "node":"........", "data":["","A1","","A1"]
		}             
		,{ "wave":"22.2....", "name":"wdat",
		   "node":"........", "data":["","D1"]
		}
		]
		,{ "wave":"2x..2.x.", "name":"rdat",
		   "node":"........", "data":["","D1"]
		}
      ]
      , "foot":{"text":"wave 讀寫實例"}  
	}


.. _arch: 

..
	marker


.. uml::
	:caption: arch 架構

	ditaa(-E -S, scale=1.2)
	+-----------+ +------------------------+
 	| cBLU      | | cGRE                   |
 	| top       | | libpattern.so          |
	|           | +-----------+ +----------+
	|  +--------+ | cBLU      | | cRED     |
	|  | DUT    | | libreg.so | | librw.so |
	|  | reg_if +-+           +-+          |
	|  +--------+ +-----------+ +----------+
	|           | | cGRE                   |
	+-----------+ +------------------------+


---------------------
case2 模組取代
---------------------

接下來我們在案例2中利用CVPI實作出reg_if，實作的結果放在libreg.so。除了libreg.so外，我們還需要更改libpattern.so來啟動/關閉實作reg_if的程式碼；同時也許要讓實例1中的reg_if成為一個只包含輸入/輸出的空模組，以避免訊號同時會有多個改變的來源。

---------------------
參數取代
---------------------

如 wave2_ 相較case1，case3的verilog引進了一些訊號：req、ack以及seq_ack。當req為1時，代表要對adr/wdat處理，直到ack為1結束。ack是否為1，是由8位元的seq_ack來決定。seq_ack在每個clock時向左移1位元，而當seq_ack的最高位元為1時，ack也同時為1。由於seq_ack有限的位元數，摸擬adr/wdat處理時間長於seq_ack的位元數時，seq_ack需要動態地更動給值。

針對上面seq_ack的問題：case3具有命令列指定參數，可以動態地更動seq_ack而產生不一樣的測試項目(pattern)，而不需要從新翻譯。針對這種動態更動參數引起了一個想法，我們可不可以利用CVPI來實現這個動態更動參數。case4/case5就是對這個想法的實現。case4是利用註冊/觸動callback函數;而case5則是利用內嵌腳本語言(python)，使用這個腳本語言動態地更動seq_ack。

動態更動參數可以分為決定可更動時機和參數更動後的值。在case4中，libreg.so包含trig_task在建立時就有一個(callback函數以及無型態指標)與reason對應表格，其中reason對應到可更動時機。trig_task當reason成立或者說可更動時機觸發時，呼叫callback函數並傳入無型態指標。libpattern.so負責同時啟動trig_tsk以及傳入對應表格，以及實作callback函數。被呼叫的callback函數會利用sig_base取得呼叫時訊號的值以及想要更改的值。

..
	除了上述描述外，每一個callback函數以及trig_task開始都有一個額外的參數，這個參數是用來作為在時間上註冊以後的呼叫callback函數的時間。當時間為0時，代表不註冊callback函數。

在case5中，利用generator機制來實作當reason成立時呼叫callback函數。generator機制可以讓python的函數暫停等待reason成立；當reason成立後，再繼續執行函數。這個generator實作當reason成立時呼叫callback函數，主要實現在libpyvpi.so。generator的使用方式可以參考python的規格書。因此我們利用generator機制來決定可以更動的時機；然後利用libpyvpi.so裏面中的sig_base來讀取以及更改值。


.. _wave2:

..
	marker

.. wavedrom::

	{ "signal" : [
		 { "wave":"p...|....|...", "name":"clk",
		   "node":".............", "data":[] }
		,{ "wave":"01..|.01.|.0.", "name":"req",
		   "node":".............", "data":[] }
		,{ "wave":"0...|10..|10.", "name":"ack",
		   "node":".............", "data":[] }
		,{ "wave":"x.2222222222.", "name":"seq_ack",
		   "node":".............", "data":["V", "V<<1","","0x80","0","V","V<<1","","0x80","0"] }
		,{ "wave":"01..|.01.|.0.", "name":"cs",
		   "node":".............", "data":[] }
		,{ "wave":"01..|.0..|...", "name":"wr",
		   "node":".............", "data":[] }
		,{ "wave":"x2..|.x2.|.x.", "name":"adr",
		   "node":".............", "data":["A1","A1"] }
		,{ "wave":"x2..|.x..|...", "name":"wdat",
		   "node":".............", "data":["D1"] }
		,{ "wave":"x...|....|2x.", "name":"rdat",
		   "node":".............", "data":["D1"] }
      ]
      , "foot":{"text":"wave2 req/ack wave 讀寫實例"}  
	}



==========
結論
==========
