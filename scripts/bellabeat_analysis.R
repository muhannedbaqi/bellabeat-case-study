bellabeat_clean <- read_csv("bellabeat_merged_clean.csv")

daily_avg_steps <- bellabeat_clean %>%
  group_by(Date) %>%
  summarise(AvgSteps = mean(TotalSteps, na.rm = TRUE)) %>%
  pull(AvgSteps) %>%
  mean(na.rm = TRUE)


hourly_peaks <- hourly_steps %>%
  mutate(Hour = hour(ActivityHour)) %>%
  group_by(Hour) %>%
  summarise(AvgSteps = mean(StepTotal, na.rm = TRUE)) %>%
  filter(AvgSteps == max(AvgSteps) | AvgSteps == min(AvgSteps))

sedentary_percent <- merged_data %>%
  summarise(SedentaryHours = mean(SedentaryMinutes / 60, na.rm = TRUE),
            PercentSedentary = (SedentaryHours / 24) * 100 )

avg_sleep <- merged_data %>%
  summarise(AvgSleep = mean(TotalMinutesAsleep / 60, na.rm = TRUE)) 

sleep_inconsistency <- merged_data %>%
  group_by(Id) %>%
  summarise(
    SleepVar = sd(TotalMinutesAsleep, na.rm = TRUE)
  ) %>%
  filter(SleepVar > 120) %>%
  nrow() / n_distinct(merged_data$Id) * 100



ggplot(bellabeat_clean, aes(x = TotalSteps)) +
  geom_histogram(binwidth = 1000, fill = "steelblue") +
  geom_vline(xintercept = 7500, color = "red", linetype = "dashed") +
  labs(title = "Daily Step Distribution", x = "Steps", y = "Frequency")


ggplot(bellabeat_clean, aes(x = TotalMinutesAsleep / 60)) +
  geom_density(fill = "purple", alpha = 0.6) +
  labs(title = "Sleep Duration Distribution", 
       x = "Hours Slept", 
       y = "Density")


ggplot(hourly_peaks, aes(x = Hour, y = AvgSteps)) +
  geom_tile(aes(fill = AvgSteps), color = "white") +
  scale_fill_gradient(low = "white", high = "purple") +
  labs(title = "Hourly Activity Peaks", x = "Hour of Day", y = "Average Steps")