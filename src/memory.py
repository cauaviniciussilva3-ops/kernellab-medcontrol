from typing import List, Tuple

class MemorySimulator:
    def __init__(self, num_frames: int = 4):
        self.num_frames = num_frames

    def fifo(self, pages: List[int]) -> Tuple[List[List[int]], int, int, float]:
        frames = []
        history = []
        hits, faults = 0, 0

        for page in pages:
            if page in frames:
                hits += 1
            else:
                faults += 1
                if len(frames) < self.num_frames:
                    frames.append(page)
                else:
                    frames.pop(0)
                    frames.append(page)
            history.append(list(frames))

        rate = (faults / len(pages)) * 100
        return history, hits, faults, rate

    def lru(self, pages: List[int]) -> Tuple[List[List[int]], int, int, float]:
        frames = []
        recent_use = {}
        history = []
        hits, faults = 0, 0

        for time, page in enumerate(pages):
            if page in frames:
                hits += 1
            else:
                faults += 1
                if len(frames) < self.num_frames:
                    frames.append(page)
                else:
                    lru_page = min(frames, key=lambda p: recent_use[p])
                    frames.remove(lru_page)
                    frames.append(page)
            recent_use[page] = time
            history.append(list(frames))

        rate = (faults / len(pages)) * 100
        return history, hits, faults, rate

    def optimal(self, pages: List[int]) -> Tuple[List[List[int]], int, int, float]:
        frames = []
        history = []
        hits, faults = 0, 0

        for i, page in enumerate(pages):
            if page in frames:
                hits += 1
            else:
                faults += 1
                if len(frames) < self.num_frames:
                    frames.append(page)
                else:
                    future_indices = {}
                    for f in frames:
                        try:
                            idx = pages[i + 1:].index(f)
                        except ValueError:
                            idx = float('inf')
                        future_indices[f] = idx

                    page_to_remove = max(frames, key=lambda f: future_indices[f])
                    frames.remove(page_to_remove)
                    frames.append(page)
            history.append(list(frames))

        rate = (faults / len(pages)) * 100
        return history, hits, faults, rate