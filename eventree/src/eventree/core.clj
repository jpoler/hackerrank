(ns eventree.core)

(require '[clojure.string :as str])

(defn read-int-line
  []
  (map #(Integer. %) (str/split (read-line) #" ")))


(defn positive-numbers
  ([] (positive-numbers 1))
  ([n] (cons n (lazy-seq (positive-numbers (inc n))))))

(defn build-graph-map
  [n]
  (loop [G (hash-map)
         ints (take n (positive-numbers))]
    (if (empty? ints)
      G
      (recur (assoc G (first ints) [])
             (rest ints)))))

(defn insert-edge
  [G pair]
  (update-in (update-in G [(first pair)] #(conj % (second pair)))
             [(second pair)] #(conj % (first pair))))

(defn insert-edges
  [n G]
  (if (= n 0)
    G
    (insert-edges (dec n) (insert-edge G (read-int-line)))))
  
(defn build-graph
  [V E]
  (insert-edges E (build-graph-map V)))

(defn find-maximum-removals-iter
  [G start parent]
  (let [connections (G start)]
    (loop [children connections
           removals 0
           subtree-count 0]
      (if (empty? children)
        (do 
          (list removals (+ subtree-count 1)))
        (if (= (first children) parent)
          (recur (rest children) removals subtree-count)
          (let [[r c] (find-maximum-removals-iter G (first children) start)]
            ;; (println "subtree of " (first children) c r)
            (if (even? c)
              (do 
                ;; (println "removing")
                (recur (rest children) (+ removals 1 r) subtree-count))
              (recur (rest children) (+ removals r) (+ subtree-count c)))))))))
  
    
(defn find-maximum-removals
  [G]
  (first (find-maximum-removals-iter G 1 0)))
  

(defn -main
  []
  (let [[V E] (read-int-line)]
    (let [G (build-graph V E)]
      ;; (println "graph " G)
      (println (find-maximum-removals G)))))
