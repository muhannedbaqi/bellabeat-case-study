### Data Cleaning & Manipulation Steps

### Data manipulation
library(tidyverse)
### Date/time formatting
library(lubridate)
### Clean column names (optional)
library(janitor)


### Import individual datasets
daily_activity <- read_csv("dailyActivity_merged.csv")
hourly_steps <- read_csv("hourlySteps_merged.csv")
sleep_data <- read_csv("sleepDay_merged.csv")

### Remove Duplicates
daily_activity <- daily_activity %>% distinct()
hourly_steps <- hourly_steps %>% distinct()
sleep_data <- sleep_data %>% distinct()

### Convert dates to Date type (adjust format if needed)
daily_activity <- daily_activity %>%
  mutate(ActivityDate = mdy(ActivityDate))

sleep_data <- sleep_data %>%
  mutate(SleepDay = mdy_hms(SleepDay))

hourly_steps <- hourly_steps %>%
  mutate(ActivityHour = mdy_hm(ActivityHour))

### Replace NA steps with 0 (if intentional inactivity)
daily_activity <- daily_activity %>%
  mutate(TotalSteps = replace_na(TotalSteps, 0))

### Impute missing sleep minutes with median
median_sleep <- median(sleep_data$TotalMinutesAsleep, na.rm = TRUE)
sleep_data <- sleep_data %>%
  mutate(TotalMinutesAsleep = replace_na(TotalMinutesAsleep, median_sleep))


### Rename columns for consistency
daily_activity <- daily_activity %>% rename(Date = ActivityDate)
sleep_data <- sleep_data %>% rename(Date = SleepDay)
hourly_steps <- hourly_steps %>% rename(Date = ActivityHour)

### Merge daily activity with sleep data
merged_data <- daily_activity %>%
  left_join(sleep_data, by = c("Id", "Date"))

merged_data <- merged_data %>%
  left_join(hourly_steps, by = c("Id", "Date"))


### Remove rows with missing steps
merged_data <- merged_data %>%
  filter(!is.na(TotalSteps))

### Calculate Derived Metrics
merged_data <- merged_data %>%
  mutate(
    ActivityLevel = case_when(
      TotalSteps < 5000 ~ "Sedentary",
      TotalSteps >= 5000 & TotalSteps < 10000 ~ "Moderate",
      TotalSteps >= 10000 ~ "Active"
    ))

### Look for mismatched IDs/dates
anti_join(daily_activity, sleep_data, by = c("Id", "Date"))

### Summarize data
glimpse(merged_data)
summary(merged_data)

write_csv(merged_data, "bellabeat_merged_clean.csv")
write_csv(hourly_steps, "hourly_steps_clean.csv")