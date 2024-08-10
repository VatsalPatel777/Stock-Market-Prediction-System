lf.getSentiments()
        count_0 = 0
        count_1 = 0
        count = 0
        for score in self.news['compound']:
            if score == 0:
                count_0 += 1
            elif score == 1:
                count_1 += 1
            else:
                count += 1
        y = [count_0, count_1, count]
        myLabels = [f"0:{count_0}", f"1:{count_1}", f"-1:{count}"]
        colors = ["#FFFF00", "#00FF00", "#FF0000"]
        fig = px.pie(values=y, names=myLabels, title="Sentiment Analysis", color=myLabels)
        return 